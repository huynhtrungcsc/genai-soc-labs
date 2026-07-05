from datetime import UTC, datetime

from app.schemas import AssetRecord, IntelRequest
from app.services.scoring import assess_intelligence, match_products


def test_product_matching_is_normalized() -> None:
    matches = match_products(["Ivanti Connect Secure"], ["ivanti-connect-secure", "Linux"])

    assert matches == ["Ivanti Connect Secure"]


def test_active_exploitation_against_exposed_critical_asset_is_critical() -> None:
    asset = AssetRecord(
        id="asset-1",
        hostname="vpn-edge-01",
        owner="network-security",
        business_unit="infrastructure",
        environment="production",
        criticality=5,
        technologies=["Ivanti Connect Secure", "Linux"],
        internet_exposed=True,
        data_classification="internal",
        tags=["edge"],
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    item = IntelRequest(
        source="CISA KEV",
        title="Active exploitation reported for Ivanti Connect Secure gateway vulnerability",
        summary="Threat report describes exploitation of exposed appliances.",
        affected_products=["Ivanti Connect Secure"],
        industries=["financial-services"],
        cves=["CVE-2025-0282"],
        iocs=["198.51.100.77"],
        mitre_techniques=["T1190"],
        observed_exploitation=True,
        severity="critical",
        confidence="high",
    )

    assessment = assess_intelligence(item, [asset])

    assert assessment.priority == "critical"
    assert assessment.relevance_score >= 90
    assert assessment.affected_assets[0].hostname == "vpn-edge-01"
    assert assessment.affected_assets[0].patch_sla == "24 hours"
