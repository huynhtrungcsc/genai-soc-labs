import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings
from app.schemas import AuditEvent, ExecutionResult, QueryJob, QueryRequest
from app.services.generator import generate_query


def _json_default(value: object) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _db_path() -> Path:
    path = get_settings().database_path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS query_jobs (
              id TEXT PRIMARY KEY,
              question TEXT NOT NULL,
              dialect TEXT NOT NULL,
              time_range TEXT NOT NULL,
              data_source TEXT NOT NULL,
              owner TEXT NOT NULL DEFAULT 'soc-hunter',
              purpose TEXT NOT NULL DEFAULT 'threat_hunt',
              max_rows INTEGER NOT NULL DEFAULT 100,
              status TEXT NOT NULL DEFAULT 'draft',
              approved_by TEXT,
              approved_at TEXT,
              generated_json TEXT NOT NULL,
              execution_json TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
              id TEXT PRIMARY KEY,
              actor TEXT NOT NULL,
              action TEXT NOT NULL,
              target_id TEXT NOT NULL,
              detail TEXT NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
        _ensure_columns(conn)


def _ensure_columns(conn: sqlite3.Connection) -> None:
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(query_jobs)").fetchall()}
    columns = {
        "owner": "TEXT NOT NULL DEFAULT 'soc-hunter'",
        "purpose": "TEXT NOT NULL DEFAULT 'threat_hunt'",
        "max_rows": "INTEGER NOT NULL DEFAULT 100",
        "status": "TEXT NOT NULL DEFAULT 'draft'",
        "approved_by": "TEXT",
        "approved_at": "TEXT",
    }
    for name, definition in columns.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE query_jobs ADD COLUMN {name} {definition}")


def create_query_job(payload: QueryRequest) -> QueryJob:
    now = datetime.now(UTC)
    job = QueryJob(
        id=str(uuid4()),
        question=payload.question,
        dialect=payload.dialect,
        time_range=payload.time_range,
        data_source=payload.data_source,
        owner=payload.owner,
        purpose=payload.purpose,
        max_rows=payload.max_rows,
        generated=generate_query(payload),
        created_at=now,
        updated_at=now,
    )
    save_query_job(job)
    return job


def save_query_job(job: QueryJob) -> None:
    job.updated_at = datetime.now(UTC)
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO query_jobs (
              id, question, dialect, time_range, data_source, owner, purpose, max_rows,
              status, approved_by, approved_at, generated_json, execution_json, created_at,
              updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              question=excluded.question,
              dialect=excluded.dialect,
              time_range=excluded.time_range,
              data_source=excluded.data_source,
              owner=excluded.owner,
              purpose=excluded.purpose,
              max_rows=excluded.max_rows,
              status=excluded.status,
              approved_by=excluded.approved_by,
              approved_at=excluded.approved_at,
              generated_json=excluded.generated_json,
              execution_json=excluded.execution_json,
              updated_at=excluded.updated_at
            """,
            (
                job.id,
                job.question,
                job.dialect,
                job.time_range,
                job.data_source,
                job.owner,
                job.purpose,
                job.max_rows,
                job.status,
                job.approved_by,
                job.approved_at.isoformat() if job.approved_at else None,
                job.generated.model_dump_json(),
                job.execution.model_dump_json() if job.execution else None,
                job.created_at.isoformat(),
                job.updated_at.isoformat(),
            ),
        )


def list_query_jobs() -> list[QueryJob]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM query_jobs ORDER BY created_at DESC").fetchall()
    return [_job_from_row(row) for row in rows]


def get_query_job(job_id: str) -> QueryJob | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM query_jobs WHERE id = ?", (job_id,)).fetchone()
    return _job_from_row(row) if row else None


def attach_execution(job: QueryJob, execution: ExecutionResult) -> QueryJob:
    job.execution = execution
    job.status = "executed"
    save_query_job(job)
    return job


def approve_query_job(job: QueryJob, approver: str) -> QueryJob:
    job.status = "approved"
    job.approved_by = approver
    job.approved_at = datetime.now(UTC)
    save_query_job(job)
    return job


def _job_from_row(row: sqlite3.Row) -> QueryJob:
    return QueryJob(
        id=row["id"],
        question=row["question"],
        dialect=row["dialect"],
        time_range=row["time_range"],
        data_source=row["data_source"],
        owner=row["owner"],
        purpose=row["purpose"],
        max_rows=row["max_rows"],
        status=row["status"],
        approved_by=row["approved_by"],
        approved_at=datetime.fromisoformat(row["approved_at"]) if row["approved_at"] else None,
        generated=json.loads(row["generated_json"]),
        execution=json.loads(row["execution_json"]) if row["execution_json"] else None,
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def record_audit(actor: str, action: str, target_id: str, detail: str) -> AuditEvent:
    event = AuditEvent(
        id=str(uuid4()),
        actor=actor,
        action=action,
        target_id=target_id,
        detail=detail,
        created_at=datetime.now(UTC),
    )
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO audit_events (id, actor, action, target_id, detail, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                event.id,
                event.actor,
                event.action,
                event.target_id,
                event.detail,
                event.created_at.isoformat(),
            ),
        )
    return event


def list_audit_events(target_id: str | None = None) -> list[AuditEvent]:
    with connect() as conn:
        if target_id:
            rows = conn.execute(
                "SELECT * FROM audit_events WHERE target_id = ? ORDER BY created_at DESC",
                (target_id,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM audit_events ORDER BY created_at DESC").fetchall()
    return [
        AuditEvent(
            id=row["id"],
            actor=row["actor"],
            action=row["action"],
            target_id=row["target_id"],
            detail=row["detail"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
        for row in rows
    ]
