from app.schemas import Incident, ResponseTask


def build_response_plan(incident: Incident) -> list[ResponseTask]:
    tasks = [
        ResponseTask(
            id="preserve-evidence",
            title="Preserve raw logs and investigation evidence",
            owner_role="incident-commander",
            rationale=(
                "Evidence must remain available for validation, reporting, "
                "and lessons learned."
            ),
            requires_approval=False,
        )
    ]
    tactics = {item.tactic for item in incident.mitre}
    if "Credential Access" in tactics or "Initial Access" in tactics:
        tasks.append(
            ResponseTask(
                id="identity-containment",
                title="Reset affected credentials and review MFA posture",
                owner_role="identity-admin",
                rationale="Account compromise can re-open access even after endpoint cleanup.",
            )
        )
    if "Execution" in tactics:
        tasks.append(
            ResponseTask(
                id="endpoint-collection",
                title="Collect process, script, and command-line telemetry",
                owner_role="edr-analyst",
                rationale="Execution evidence is needed to confirm payload behavior and scope.",
                requires_approval=False,
            )
        )
    if "Lateral Movement" in tactics:
        tasks.append(
            ResponseTask(
                id="network-scope",
                title="Scope SMB and privileged session activity across adjacent hosts",
                owner_role="soc-tier2",
                rationale="Lateral movement can expand the incident beyond the initial host.",
            )
        )
    if "Command and Control" in tactics:
        tasks.append(
            ResponseTask(
                id="block-c2",
                title="Block confirmed C2 indicators after analyst validation",
                owner_role="network-security",
                rationale="Network containment reduces attacker control while preserving approval.",
            )
        )
    if "Impact" in tactics:
        tasks.append(
            ResponseTask(
                id="recovery-readiness",
                title="Validate backups and prepare recovery plan",
                owner_role="infrastructure",
                rationale=(
                    "Impact activity requires recovery readiness before "
                    "restoration decisions."
                ),
            )
        )
    return tasks
