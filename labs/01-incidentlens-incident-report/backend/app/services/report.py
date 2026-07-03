from app.schemas import Incident, ReportBundle


def generate_reports(incident: Incident) -> ReportBundle:
    technical = "\n".join(
        [
            f"# Technical Incident Report: {incident.title}",
            "",
            f"- Severity: {incident.severity.upper()}",
            f"- Status: {incident.status}",
            f"- Owner: {incident.owner}",
            f"- Environment: {incident.environment}",
            f"- Events analyzed: {len(incident.events)}",
            f"- MITRE techniques mapped: {len(incident.mitre)}",
            f"- Risk score: {_risk_line(incident)}",
            "",
            "## Analyst Summary",
            incident.summary or "No analyst summary was provided.",
            "",
            "## Business Context",
            _business_context(incident),
            "",
            "## Timeline",
            *_timeline_lines(incident),
            "",
            "## MITRE ATT&CK Mapping",
            *_mitre_lines(incident),
            "",
            "## Data Quality",
            *_quality_lines(incident),
            "",
            "## Recommended Response",
            *_response_task_lines(incident),
            "",
            "## Evidence Handling",
            "Preserve raw logs, endpoint telemetry, account activity, and network indicators. "
            "Validate every inference against source evidence before distribution.",
        ]
    )
    executive = "\n".join(
        [
            f"# Executive Brief: {incident.title}",
            "",
            (
                f"Current severity is **{incident.severity.upper()}** based on "
                f"{len(incident.events)} analyzed events."
            ),
            f"Current risk score is **{_risk_line(incident)}**.",
            "",
            "## What Happened",
            _executive_narrative(incident),
            "",
            "## Business Risk",
            _business_risk(incident),
            "",
            "## Immediate Actions",
            *_executive_actions(incident),
        ]
    )
    return ReportBundle(technical=technical, executive=executive)


def _timeline_lines(incident: Incident) -> list[str]:
    if not incident.timeline:
        return ["No timeline could be built from the provided events."]
    lines: list[str] = []
    for step in incident.timeline:
        timestamp = step.timestamp.isoformat() if step.timestamp else "unknown time"
        lines.extend(
            [
                f"### {step.phase}",
                f"- Time: {timestamp}",
                f"- Finding: {step.title}",
                f"- Inference: {step.inference}",
                f"- Confidence: {step.confidence:.2f}",
                "- Evidence:",
                *[f"  - {item}" for item in step.evidence],
                "",
            ]
        )
    return lines


def _mitre_lines(incident: Incident) -> list[str]:
    if not incident.mitre:
        return ["No MITRE ATT&CK techniques were mapped."]
    lines: list[str] = []
    for item in incident.mitre:
        lines.extend(
            [
                f"- {item.tactic}: {item.technique_id} {item.technique} "
                f"(confidence {item.confidence:.2f})",
                *[f"  - Evidence: {evidence}" for evidence in item.evidence[:3]],
            ]
        )
    return lines


def _recommendations(incident: Incident) -> list[str]:
    tactics = {item.tactic for item in incident.mitre}
    recommendations = [
        "- Assign an incident owner and confirm the investigation timeline.",
        "- Preserve raw evidence and keep a clear chain of custody.",
    ]
    if "Credential Access" in tactics or "Initial Access" in tactics:
        recommendations.append("- Reset affected credentials and review MFA posture.")
    if "Execution" in tactics:
        recommendations.append(
            "- Collect process, script, and command-line telemetry from affected hosts."
        )
    if "Lateral Movement" in tactics:
        recommendations.append(
            "- Review privileged sessions, SMB access, and administrative share usage."
        )
    if "Command and Control" in tactics:
        recommendations.append(
            "- Block confirmed C2 indicators and hunt for similar beaconing patterns."
        )
    if "Impact" in tactics:
        recommendations.append("- Start recovery planning and validate backups before restoration.")
    return recommendations


def _quality_lines(incident: Incident) -> list[str]:
    if not incident.data_quality:
        return ["No data quality issues were identified."]
    return [
        f"- {finding.severity.upper()} `{finding.field}`: {finding.message}"
        for finding in incident.data_quality
    ]


def _response_task_lines(incident: Incident) -> list[str]:
    if not incident.response_tasks:
        return _recommendations(incident)
    return [
        f"- [{task.status}] {task.title} ({task.owner_role}) - {task.rationale}"
        for task in incident.response_tasks
    ]


def _executive_actions(incident: Incident) -> list[str]:
    if not incident.response_tasks:
        return [
            "- Confirm scope and affected systems.",
            "- Contain suspicious accounts or hosts after analyst approval.",
            "- Preserve evidence for post-incident review.",
            "- Communicate status updates using a single incident owner.",
        ]
    return [f"- {task.title}" for task in incident.response_tasks[:4]]


def _risk_line(incident: Incident) -> str:
    if not incident.risk:
        return "not assessed"
    return (
        f"{incident.risk.score}/100 "
        f"({incident.risk.level.upper()}, SLA: {incident.risk.recommended_sla})"
    )


def _business_context(incident: Incident) -> str:
    assets = ", ".join(incident.affected_assets) if incident.affected_assets else "Not declared"
    impact = incident.business_impact or "Not declared"
    tags = ", ".join(incident.tags) if incident.tags else "none"
    return "\n".join(
        [
            f"- Affected assets: {assets}",
            f"- Business impact: {impact}",
            f"- Tags: {tags}",
        ]
    )


def _executive_narrative(incident: Incident) -> str:
    if not incident.timeline:
        return "Security events were received, but the attack sequence is not yet clear."
    phases = ", ".join(step.phase for step in incident.timeline)
    return f"The observed activity currently maps to these phases: {phases}."


def _business_risk(incident: Incident) -> str:
    if incident.severity in {"critical", "high"}:
        return (
            "The incident may affect service availability, data protection, "
            "or operational trust."
        )
    return (
        "The incident should be investigated, but current evidence does not yet "
        "indicate severe business impact."
    )
