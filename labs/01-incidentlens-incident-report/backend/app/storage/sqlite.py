import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings
from app.schemas import AuditEvent, Incident, IncidentCreate, IncidentStatus


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
            CREATE TABLE IF NOT EXISTS incidents (
              id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              severity TEXT NOT NULL,
              status TEXT NOT NULL DEFAULT 'new',
              owner TEXT NOT NULL DEFAULT 'soc-tier1',
              environment TEXT NOT NULL DEFAULT 'production',
              summary TEXT NOT NULL,
              business_impact TEXT NOT NULL DEFAULT '',
              affected_assets_json TEXT NOT NULL DEFAULT '[]',
              tags_json TEXT NOT NULL DEFAULT '[]',
              raw_logs TEXT NOT NULL,
              events_json TEXT NOT NULL,
              timeline_json TEXT NOT NULL,
              mitre_json TEXT NOT NULL,
              data_quality_json TEXT NOT NULL DEFAULT '[]',
              risk_json TEXT,
              response_tasks_json TEXT NOT NULL DEFAULT '[]',
              reports_json TEXT,
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
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(incidents)").fetchall()}
    columns = {
        "status": "TEXT NOT NULL DEFAULT 'new'",
        "owner": "TEXT NOT NULL DEFAULT 'soc-tier1'",
        "environment": "TEXT NOT NULL DEFAULT 'production'",
        "business_impact": "TEXT NOT NULL DEFAULT ''",
        "affected_assets_json": "TEXT NOT NULL DEFAULT '[]'",
        "tags_json": "TEXT NOT NULL DEFAULT '[]'",
        "data_quality_json": "TEXT NOT NULL DEFAULT '[]'",
        "risk_json": "TEXT",
        "response_tasks_json": "TEXT NOT NULL DEFAULT '[]'",
    }
    for name, definition in columns.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE incidents ADD COLUMN {name} {definition}")


def create_incident(payload: IncidentCreate) -> Incident:
    now = datetime.now(UTC)
    incident = Incident(
        id=str(uuid4()),
        title=payload.title,
        severity=payload.severity,
        owner=payload.owner,
        environment=payload.environment,
        summary=payload.summary,
        business_impact=payload.business_impact,
        affected_assets=payload.affected_assets,
        tags=payload.tags,
        raw_logs=payload.raw_logs,
        created_at=now,
        updated_at=now,
    )
    save_incident(incident)
    return incident


def save_incident(incident: Incident) -> None:
    incident.updated_at = datetime.now(UTC)
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO incidents (
              id, title, severity, status, owner, environment, summary, business_impact,
              affected_assets_json, tags_json, raw_logs, events_json, timeline_json,
              mitre_json, data_quality_json, risk_json, response_tasks_json, reports_json,
              created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              title=excluded.title,
              severity=excluded.severity,
              status=excluded.status,
              owner=excluded.owner,
              environment=excluded.environment,
              summary=excluded.summary,
              business_impact=excluded.business_impact,
              affected_assets_json=excluded.affected_assets_json,
              tags_json=excluded.tags_json,
              raw_logs=excluded.raw_logs,
              events_json=excluded.events_json,
              timeline_json=excluded.timeline_json,
              mitre_json=excluded.mitre_json,
              data_quality_json=excluded.data_quality_json,
              risk_json=excluded.risk_json,
              response_tasks_json=excluded.response_tasks_json,
              reports_json=excluded.reports_json,
              updated_at=excluded.updated_at
            """,
            (
                incident.id,
                incident.title,
                incident.severity,
                incident.status,
                incident.owner,
                incident.environment,
                incident.summary,
                incident.business_impact,
                json.dumps(incident.affected_assets),
                json.dumps(incident.tags),
                incident.raw_logs,
                json.dumps(
                    [event.model_dump() for event in incident.events],
                    default=_json_default,
                ),
                json.dumps(
                    [step.model_dump() for step in incident.timeline],
                    default=_json_default,
                ),
                json.dumps([item.model_dump() for item in incident.mitre], default=_json_default),
                json.dumps(
                    [finding.model_dump() for finding in incident.data_quality],
                    default=_json_default,
                ),
                incident.risk.model_dump_json() if incident.risk else None,
                json.dumps(
                    [task.model_dump() for task in incident.response_tasks],
                    default=_json_default,
                ),
                incident.reports.model_dump_json() if incident.reports else None,
                incident.created_at.isoformat(),
                incident.updated_at.isoformat(),
            ),
        )


def _incident_from_row(row: sqlite3.Row) -> Incident:
    return Incident(
        id=row["id"],
        title=row["title"],
        severity=row["severity"],
        status=row["status"],
        owner=row["owner"],
        environment=row["environment"],
        summary=row["summary"],
        business_impact=row["business_impact"],
        affected_assets=json.loads(row["affected_assets_json"]),
        tags=json.loads(row["tags_json"]),
        raw_logs=row["raw_logs"],
        events=json.loads(row["events_json"]),
        timeline=json.loads(row["timeline_json"]),
        mitre=json.loads(row["mitre_json"]),
        data_quality=json.loads(row["data_quality_json"]),
        risk=json.loads(row["risk_json"]) if row["risk_json"] else None,
        response_tasks=json.loads(row["response_tasks_json"]),
        reports=json.loads(row["reports_json"]) if row["reports_json"] else None,
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def list_incidents() -> list[Incident]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM incidents ORDER BY created_at DESC").fetchall()
    return [_incident_from_row(row) for row in rows]


def get_incident(incident_id: str) -> Incident | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    return _incident_from_row(row) if row else None


def update_incident_status(incident: Incident, status: IncidentStatus) -> Incident:
    incident.status = status
    save_incident(incident)
    return incident


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
