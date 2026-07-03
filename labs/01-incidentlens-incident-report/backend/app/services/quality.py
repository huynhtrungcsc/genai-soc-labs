from app.schemas import DataQualityFinding, NormalizedEvent


def assess_data_quality(events: list[NormalizedEvent]) -> list[DataQualityFinding]:
    findings: list[DataQualityFinding] = []
    if not events:
        return [
            DataQualityFinding(
                severity="error",
                field="raw_logs",
                message="No parseable events were found in the submitted evidence.",
            )
        ]

    missing_timestamps = sum(1 for event in events if event.timestamp is None)
    missing_hosts = sum(1 for event in events if event.host == "unknown")
    missing_users = sum(1 for event in events if event.user == "unknown")

    if missing_timestamps:
        findings.append(
            DataQualityFinding(
                severity="warning",
                field="timestamp",
                message=f"{missing_timestamps} events do not include a parseable timestamp.",
            )
        )
    if missing_hosts:
        findings.append(
            DataQualityFinding(
                severity="warning",
                field="host",
                message=f"{missing_hosts} events are missing host context.",
            )
        )
    if missing_users:
        findings.append(
            DataQualityFinding(
                severity="info",
                field="user",
                message=f"{missing_users} events are missing user context.",
            )
        )
    if len({event.source for event in events}) < 2:
        findings.append(
            DataQualityFinding(
                severity="warning",
                field="source",
                message=(
                    "Only one log source is present. Corroborate with EDR, "
                    "identity, or network logs."
                ),
            )
        )
    return findings
