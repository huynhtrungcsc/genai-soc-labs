from datetime import UTC, datetime

from app.schemas import BriefingRequest, IntelRecord, IntelRequest
from app.services.briefing import generate_briefing
from app.services.scoring import assess_intelligence


def test_patch_briefing_uses_asset_sla() -> None:
    request = IntelRequest(
        source="Vendor Advisory",
        title="Apache Struts exploit attempts observed against internet-facing Java applications",
        summary="Observed scanning and exploit attempts against vulnerable web applications.",
        affected_products=["Apache Struts"],
        industries=["financial-services"],
        cves=["CVE-2026-23010"],
        observed_exploitation=True,
        severity="critical",
        confidence="high",
    )
    assessment = assess_intelligence(request, [])
    item = IntelRecord(
        id="intel-1",
        assessment=assessment,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        **request.model_dump(),
    )

    briefing = generate_briefing(
        BriefingRequest(audience="patch", lookback_days=30, max_items=5),
        [item],
    )

    assert briefing.audience == "patch"
    assert briefing.sections[0].priority == "critical"
    assert "No patch queue entry" in briefing.sections[0].summary
    assert briefing.status == "draft"
