import json
import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings
from app.schemas import (
    AssetRecord,
    AssetRequest,
    AuditEvent,
    Briefing,
    BriefingRequest,
    IntelRecord,
    IntelRequest,
)
from app.services.briefing import generate_briefing
from app.services.scoring import assess_intelligence


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
            CREATE TABLE IF NOT EXISTS assets (
              id TEXT PRIMARY KEY,
              hostname TEXT NOT NULL,
              body_json TEXT NOT NULL,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS intel_items (
              id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              source TEXT NOT NULL,
              severity TEXT NOT NULL,
              priority TEXT NOT NULL,
              relevance_score INTEGER NOT NULL,
              observed_exploitation INTEGER NOT NULL,
              published_at TEXT NOT NULL,
              body_json TEXT NOT NULL,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS briefings (
              id TEXT PRIMARY KEY,
              audience TEXT NOT NULL,
              status TEXT NOT NULL,
              owner TEXT NOT NULL,
              title TEXT NOT NULL,
              body_json TEXT NOT NULL,
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


def create_asset(payload: AssetRequest) -> AssetRecord:
    now = datetime.now(UTC)
    asset = AssetRecord(id=str(uuid4()), created_at=now, updated_at=now, **payload.model_dump())
    save_asset(asset)
    return asset


def bulk_create_assets(payloads: Iterable[AssetRequest]) -> list[AssetRecord]:
    return [create_asset(payload) for payload in payloads]


def save_asset(asset: AssetRecord) -> None:
    asset.updated_at = datetime.now(UTC)
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO assets (id, hostname, body_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              hostname=excluded.hostname,
              body_json=excluded.body_json,
              updated_at=excluded.updated_at
            """,
            (
                asset.id,
                asset.hostname,
                asset.model_dump_json(),
                asset.created_at.isoformat(),
                asset.updated_at.isoformat(),
            ),
        )


def list_assets() -> list[AssetRecord]:
    with connect() as conn:
        rows = conn.execute("SELECT body_json FROM assets ORDER BY hostname ASC").fetchall()
    return [AssetRecord.model_validate_json(row["body_json"]) for row in rows]


def get_asset(asset_id: str) -> AssetRecord | None:
    with connect() as conn:
        row = conn.execute("SELECT body_json FROM assets WHERE id = ?", (asset_id,)).fetchone()
    return AssetRecord.model_validate_json(row["body_json"]) if row else None


def create_intel_item(payload: IntelRequest) -> IntelRecord:
    now = datetime.now(UTC)
    assessment = assess_intelligence(payload, list_assets())
    item = IntelRecord(
        id=str(uuid4()),
        assessment=assessment,
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    save_intel_item(item)
    return item


def save_intel_item(item: IntelRecord) -> None:
    item.updated_at = datetime.now(UTC)
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO intel_items (
              id, title, source, severity, priority, relevance_score,
              observed_exploitation, published_at, body_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              title=excluded.title,
              source=excluded.source,
              severity=excluded.severity,
              priority=excluded.priority,
              relevance_score=excluded.relevance_score,
              observed_exploitation=excluded.observed_exploitation,
              published_at=excluded.published_at,
              body_json=excluded.body_json,
              updated_at=excluded.updated_at
            """,
            (
                item.id,
                item.title,
                item.source,
                item.severity,
                item.assessment.priority,
                item.assessment.relevance_score,
                int(item.observed_exploitation),
                item.published_at.isoformat(),
                item.model_dump_json(),
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
            ),
        )


def list_intel_items() -> list[IntelRecord]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT body_json FROM intel_items ORDER BY relevance_score DESC, published_at DESC"
        ).fetchall()
    return [IntelRecord.model_validate_json(row["body_json"]) for row in rows]


def get_intel_item(item_id: str) -> IntelRecord | None:
    with connect() as conn:
        row = conn.execute("SELECT body_json FROM intel_items WHERE id = ?", (item_id,)).fetchone()
    return IntelRecord.model_validate_json(row["body_json"]) if row else None


def reassess_intel_item(item: IntelRecord) -> IntelRecord:
    item.assessment = assess_intelligence(item, list_assets())
    save_intel_item(item)
    return item


def reassess_all_intel() -> list[IntelRecord]:
    return [reassess_intel_item(item) for item in list_intel_items()]


def create_briefing(payload: BriefingRequest) -> Briefing:
    briefing = generate_briefing(payload, list_intel_items())
    save_briefing(briefing)
    return briefing


def save_briefing(briefing: Briefing) -> None:
    briefing.updated_at = datetime.now(UTC)
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO briefings (
              id, audience, status, owner, title, body_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              audience=excluded.audience,
              status=excluded.status,
              owner=excluded.owner,
              title=excluded.title,
              body_json=excluded.body_json,
              updated_at=excluded.updated_at
            """,
            (
                briefing.id,
                briefing.audience,
                briefing.status,
                briefing.owner,
                briefing.title,
                briefing.model_dump_json(),
                briefing.created_at.isoformat(),
                briefing.updated_at.isoformat(),
            ),
        )


def list_briefings() -> list[Briefing]:
    with connect() as conn:
        rows = conn.execute("SELECT body_json FROM briefings ORDER BY created_at DESC").fetchall()
    return [Briefing.model_validate_json(row["body_json"]) for row in rows]


def get_briefing(briefing_id: str) -> Briefing | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT body_json FROM briefings WHERE id = ?",
            (briefing_id,),
        ).fetchone()
    return Briefing.model_validate_json(row["body_json"]) if row else None


def approve_briefing(briefing: Briefing, approver: str) -> Briefing:
    briefing.status = "approved"
    briefing.approved_by = approver
    briefing.approved_at = datetime.now(UTC)
    save_briefing(briefing)
    return briefing


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
    query = "SELECT * FROM audit_events"
    params: tuple[str, ...] = ()
    if target_id:
        query += " WHERE target_id = ?"
        params = (target_id,)
    query += " ORDER BY created_at DESC"
    with connect() as conn:
        rows = conn.execute(query, params).fetchall()
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


def export_snapshot() -> dict[str, object]:
    return {
        "assets": json.loads(
            json.dumps([asset.model_dump(mode="json") for asset in list_assets()])
        ),
        "intel_items": json.loads(
            json.dumps([item.model_dump(mode="json") for item in list_intel_items()])
        ),
        "briefings": json.loads(
            json.dumps([briefing.model_dump(mode="json") for briefing in list_briefings()])
        ),
    }
