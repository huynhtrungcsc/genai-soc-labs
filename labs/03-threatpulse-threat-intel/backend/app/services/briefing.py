from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.schemas import Briefing, BriefingRequest, BriefingSection, IntelRecord

PRIORITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def generate_briefing(payload: BriefingRequest, intel_items: list[IntelRecord]) -> Briefing:
    now = datetime.now(UTC)
    cutoff = now - timedelta(days=payload.lookback_days)
    scoped_items = [
        item
        for item in intel_items
        if item.published_at >= cutoff or item.created_at >= cutoff
    ]
    scoped_items.sort(
        key=lambda item: (
            PRIORITY_ORDER[item.assessment.priority],
            item.assessment.relevance_score,
            item.published_at,
        ),
        reverse=True,
    )
    selected = scoped_items[: payload.max_items]
    sections = [section_for_item(item, payload.audience) for item in selected]

    top_priorities = [
        f"{item.assessment.priority.upper()}: {item.title}"
        for item in selected[:3]
    ]
    patch_queue = build_patch_queue(selected)

    return Briefing(
        id=str(uuid4()),
        audience=payload.audience,
        owner=payload.owner,
        title=f"ThreatPulse {payload.audience.title()} Briefing",
        top_priorities=top_priorities,
        patch_queue=patch_queue,
        sections=sections,
        limitations=[
            "Briefing uses ingested intelligence and local asset inventory only.",
            "Asset matching is deterministic and should be validated by asset owners.",
            "No exploit instructions or offensive automation are generated.",
        ],
        generated_at=now,
        created_at=now,
        updated_at=now,
    )


def section_for_item(item: IntelRecord, audience: str) -> BriefingSection:
    summary = (
        item.assessment.executive_summary
        if audience == "executive"
        else item.assessment.analyst_summary
    )
    if audience == "patch":
        summary = build_patch_summary(item)

    return BriefingSection(
        intel_id=item.id,
        title=item.title,
        priority=item.assessment.priority,
        summary=summary,
        affected_assets=[asset.hostname for asset in item.assessment.affected_assets],
        evidence=item.assessment.evidence,
        recommended_actions=item.assessment.recommended_actions,
    )


def build_patch_summary(item: IntelRecord) -> str:
    if not item.assessment.affected_assets:
        return "No patch queue entry is required until an internal asset match is confirmed."
    highest = item.assessment.affected_assets[0]
    return (
        f"Patch focus: {highest.hostname} and related assets running "
        f"{', '.join(highest.matched_technologies)}. Target SLA: {highest.patch_sla}."
    )


def build_patch_queue(items: list[IntelRecord]) -> list[str]:
    queue: list[str] = []
    for item in items:
        for asset in item.assessment.affected_assets[:5]:
            queue.append(
                f"{asset.priority.upper()} | {asset.hostname} | "
                f"{', '.join(asset.matched_technologies)} | SLA {asset.patch_sla}"
            )
    return queue[:15]
