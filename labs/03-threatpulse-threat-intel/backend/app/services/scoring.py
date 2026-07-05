from app.schemas import (
    AffectedAsset,
    AssetRecord,
    IntelAssessment,
    IntelRequest,
    Priority,
)

SEVERITY_BASE = {
    "low": 20,
    "medium": 40,
    "high": 65,
    "critical": 82,
}

CONFIDENCE_WEIGHT = {
    "low": -8,
    "medium": 0,
    "high": 8,
}


def assess_intelligence(item: IntelRequest, assets: list[AssetRecord]) -> IntelAssessment:
    affected_assets = [_assess_asset(item, asset) for asset in assets]
    affected_assets = [asset for asset in affected_assets if asset is not None]
    affected_assets.sort(key=lambda asset: asset.risk_score, reverse=True)

    top_asset_score = affected_assets[0].risk_score if affected_assets else 0
    sector_match = _industry_match(item.industries)
    exploitation_bonus = 14 if item.observed_exploitation else 0
    cve_bonus = min(len(item.cves) * 3, 9)
    relevance_score = max(top_asset_score, SEVERITY_BASE[item.severity] + sector_match)
    relevance_score = min(100, relevance_score + exploitation_bonus + cve_bonus)

    priority = priority_from_score(relevance_score)
    evidence = build_evidence(item, affected_assets)
    actions = build_recommended_actions(item, affected_assets, priority)

    return IntelAssessment(
        relevance_score=relevance_score,
        priority=priority,
        analyst_summary=build_analyst_summary(item, affected_assets, priority),
        executive_summary=build_executive_summary(item, affected_assets, priority),
        affected_assets=affected_assets,
        recommended_actions=actions,
        evidence=evidence,
        assumptions=build_assumptions(item, affected_assets),
        tags=build_tags(item, priority),
    )


def _assess_asset(item: IntelRequest, asset: AssetRecord) -> AffectedAsset | None:
    matches = match_products(item.affected_products, asset.technologies)
    if not matches:
        return None

    score = SEVERITY_BASE[item.severity]
    score += asset.criticality * 6
    score += 12 if asset.internet_exposed else 0
    score += 14 if item.observed_exploitation else 0
    score += CONFIDENCE_WEIGHT[item.confidence]
    score += min(len(item.cves) * 2, 8)
    score = min(100, max(0, score))

    exposure_reasons = [
        f"technology match: {', '.join(matches)}",
        f"asset criticality: {asset.criticality}/5",
    ]
    if asset.internet_exposed:
        exposure_reasons.append("internet exposed asset")
    if asset.data_classification in {"restricted", "confidential"}:
        exposure_reasons.append(f"{asset.data_classification} data classification")
    if item.observed_exploitation:
        exposure_reasons.append("exploitation observed in the wild")

    priority = priority_from_score(score)
    return AffectedAsset(
        asset_id=asset.id,
        hostname=asset.hostname,
        matched_technologies=matches,
        exposure_reasons=exposure_reasons,
        risk_score=score,
        priority=priority,
        patch_sla=sla_for_priority(priority),
        rationale=(
            f"{asset.hostname} runs {', '.join(matches)} and has a computed "
            f"threat exposure score of {score}."
        ),
    )


def match_products(products: list[str], technologies: list[str]) -> list[str]:
    normalized_products = [(product, normalize(product)) for product in products]
    matches: list[str] = []
    for technology in technologies:
        normalized_technology = normalize(technology)
        for product, normalized_product in normalized_products:
            if not normalized_product:
                continue
            product_matches_asset = normalized_product in normalized_technology
            asset_matches_product = normalized_technology in normalized_product
            if product_matches_asset or asset_matches_product:
                matches.append(product)
    return sorted(set(matches))


def normalize(value: str) -> str:
    return "".join(character.lower() for character in value if character.isalnum())


def _industry_match(industries: list[str]) -> int:
    normalized = {industry.lower().replace(" ", "-") for industry in industries}
    return 10 if {"financial-services", "finance", "banking"} & normalized else 0


def priority_from_score(score: int) -> Priority:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


def sla_for_priority(priority: Priority) -> str:
    return {
        "critical": "24 hours",
        "high": "72 hours",
        "medium": "7 days",
        "low": "30 days",
    }[priority]


def build_evidence(item: IntelRequest, affected_assets: list[AffectedAsset]) -> list[str]:
    evidence = [
        f"source={item.source}",
        f"severity={item.severity}",
        f"confidence={item.confidence}",
        f"source_reliability={item.source_reliability}",
    ]
    if item.cves:
        evidence.append(f"cves={', '.join(item.cves)}")
    if item.observed_exploitation:
        evidence.append("observed_exploitation=true")
    if affected_assets:
        evidence.append(
            "affected_assets="
            + ", ".join(asset.hostname for asset in affected_assets[:5])
        )
    return evidence


def build_recommended_actions(
    item: IntelRequest,
    affected_assets: list[AffectedAsset],
    priority: Priority,
) -> list[str]:
    actions = [
        "Validate source references and vendor advisory details.",
        "Search SIEM telemetry for matching IOCs, exploit patterns, and affected hosts.",
    ]
    if affected_assets:
        actions.append("Prioritize remediation for affected assets by computed risk score.")
        highest_sla = sla_for_priority(priority)
        actions.append(f"Open patch or mitigation work item with target SLA: {highest_sla}.")
    else:
        actions.append("Monitor only; no current asset inventory match was found.")
    if item.observed_exploitation:
        actions.append("Escalate to incident response watchlist because exploitation is active.")
    if item.mitre_techniques:
        actions.append("Map detections to MITRE techniques: " + ", ".join(item.mitre_techniques))
    return actions


def build_analyst_summary(
    item: IntelRequest,
    affected_assets: list[AffectedAsset],
    priority: Priority,
) -> str:
    asset_count = len(affected_assets)
    exploit_text = (
        "with observed exploitation"
        if item.observed_exploitation
        else "without confirmed exploitation"
    )
    return (
        f"{item.title} is assessed as {priority} priority for SOC review {exploit_text}. "
        f"{asset_count} asset(s) matched the affected product set."
    )


def build_executive_summary(
    item: IntelRequest,
    affected_assets: list[AffectedAsset],
    priority: Priority,
) -> str:
    asset_text = "no known internal asset matches" if not affected_assets else (
        f"{len(affected_assets)} potentially exposed internal asset(s)"
    )
    return f"{priority.title()} priority threat intelligence item with {asset_text}: {item.summary}"


def build_assumptions(item: IntelRequest, affected_assets: list[AffectedAsset]) -> list[str]:
    assumptions = [
        "Asset matching is based on normalized product names in the local inventory.",
        "Severity and confidence are taken from the ingested intelligence source.",
    ]
    if item.references:
        assumptions.append(
            "References are treated as source citations, not as proof of exploitation."
        )
    if not affected_assets:
        assumptions.append(
            "No asset match may indicate incomplete inventory rather than no exposure."
        )
    return assumptions


def build_tags(item: IntelRequest, priority: Priority) -> list[str]:
    tags = [priority, item.severity, item.confidence]
    if item.observed_exploitation:
        tags.append("active-exploitation")
    tags.extend(technique.lower() for technique in item.mitre_techniques[:5])
    return sorted(set(tags))
