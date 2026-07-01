import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings
from app.schemas import Incident, IncidentCreate


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
              summary TEXT NOT NULL,
              raw_logs TEXT NOT NULL,
              events_json TEXT NOT NULL,
              timeline_json TEXT NOT NULL,
              mitre_json TEXT NOT NULL,
              reports_json TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )


def create_incident(payload: IncidentCreate) -> Incident:
    now = datetime.now(UTC)
    incident = Incident(
        id=str(uuid4()),
        title=payload.title,
        severity=payload.severity,
        summary=payload.summary,
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
              id, title, severity, summary, raw_logs, events_json, timeline_json,
              mitre_json, reports_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              title=excluded.title,
              severity=excluded.severity,
              summary=excluded.summary,
              raw_logs=excluded.raw_logs,
              events_json=excluded.events_json,
              timeline_json=excluded.timeline_json,
              mitre_json=excluded.mitre_json,
              reports_json=excluded.reports_json,
              updated_at=excluded.updated_at
            """,
            (
                incident.id,
                incident.title,
                incident.severity,
                incident.summary,
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
        summary=row["summary"],
        raw_logs=row["raw_logs"],
        events=json.loads(row["events_json"]),
        timeline=json.loads(row["timeline_json"]),
        mitre=json.loads(row["mitre_json"]),
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
