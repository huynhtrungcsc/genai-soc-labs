import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings
from app.schemas import ExecutionResult, QueryJob, QueryRequest
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
              generated_json TEXT NOT NULL,
              execution_json TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )


def create_query_job(payload: QueryRequest) -> QueryJob:
    now = datetime.now(UTC)
    job = QueryJob(
        id=str(uuid4()),
        question=payload.question,
        dialect=payload.dialect,
        time_range=payload.time_range,
        data_source=payload.data_source,
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
              id, question, dialect, time_range, data_source, generated_json,
              execution_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              question=excluded.question,
              dialect=excluded.dialect,
              time_range=excluded.time_range,
              data_source=excluded.data_source,
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
    save_query_job(job)
    return job


def _job_from_row(row: sqlite3.Row) -> QueryJob:
    return QueryJob(
        id=row["id"],
        question=row["question"],
        dialect=row["dialect"],
        time_range=row["time_range"],
        data_source=row["data_source"],
        generated=json.loads(row["generated_json"]),
        execution=json.loads(row["execution_json"]) if row["execution_json"] else None,
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )
