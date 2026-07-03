from app.schemas import Incident, RiskAssessment, Severity


def assess_risk(incident: Incident) -> RiskAssessment:
    score = _severity_base(incident.severity)
    drivers = [f"Declared severity is {incident.severity}."]
    tactics = {item.tactic for item in incident.mitre}

    if "Impact" in tactics:
        score += 20
        drivers.append("Impact technique observed in MITRE mapping.")
    if "Lateral Movement" in tactics:
        score += 15
        drivers.append("Lateral movement evidence increases blast radius.")
    if "Command and Control" in tactics:
        score += 12
        drivers.append("C2-like activity may indicate active compromise.")
    if "Credential Access" in tactics or "Initial Access" in tactics:
        score += 10
        drivers.append("Identity activity suggests account compromise risk.")
    if incident.business_impact:
        score += 8
        drivers.append("Business impact has been documented by the analyst.")
    if incident.affected_assets:
        score += min(10, len(incident.affected_assets) * 3)
        drivers.append(f"{len(incident.affected_assets)} affected assets were declared.")
    if any(finding.severity == "error" for finding in incident.data_quality):
        score -= 10
        drivers.append("Risk confidence reduced because evidence quality has errors.")

    score = max(0, min(100, score))
    return RiskAssessment(
        score=score,
        level=_risk_level(score),
        drivers=drivers,
        recommended_sla=_sla(score),
    )


def _severity_base(severity: Severity) -> int:
    return {"low": 20, "medium": 40, "high": 65, "critical": 80}[severity]


def _risk_level(score: int) -> Severity:
    if score >= 85:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _sla(score: int) -> str:
    if score >= 85:
        return "Contain within 1 hour and brief leadership immediately."
    if score >= 65:
        return "Contain within 4 hours and provide same-day incident update."
    if score >= 40:
        return "Triage within 1 business day and monitor for escalation."
    return "Track as low-risk investigation item."
