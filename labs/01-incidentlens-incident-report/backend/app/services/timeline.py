from app.schemas import NormalizedEvent, TimelineStep

PHASE_RULES = (
    ("Initial Access", ("successful_login", "valid accounts", "vpn")),
    ("Credential Access", ("failed_login", "brute force", "password")),
    ("Execution", ("powershell", "encodedcommand", "script")),
    ("Lateral Movement", ("lateral_movement", "smb", "admin$")),
    ("Command and Control", ("command_and_control", "beacon", "c2")),
    ("Impact", ("impact", "ransom", "encrypt")),
)


def build_timeline(events: list[NormalizedEvent]) -> list[TimelineStep]:
    steps: list[TimelineStep] = []
    for phase, keywords in PHASE_RULES:
        matches = [_event for _event in events if _matches(_event, keywords)]
        if not matches:
            continue
        first = matches[0]
        steps.append(
            TimelineStep(
                phase=phase,
                timestamp=first.timestamp,
                title=_title_for_phase(phase, first),
                evidence=[_format_evidence(event) for event in matches[:5]],
                inference=_inference_for_phase(phase),
                confidence=min(0.95, 0.62 + 0.08 * len(matches)),
            )
        )
    if not steps and events:
        first = events[0]
        steps.append(
            TimelineStep(
                phase="Observed Activity",
                timestamp=first.timestamp,
                title=(
                    "Security-relevant events were observed but no attack phase was "
                    "confidently inferred"
                ),
                evidence=[_format_evidence(event) for event in events[:5]],
                inference="More context is required before assigning a specific kill-chain phase.",
                confidence=0.35,
            )
        )
    return sorted(
        steps,
        key=lambda step: (
            step.timestamp is None,
            step.timestamp.isoformat() if step.timestamp else "",
        ),
    )


def _matches(event: NormalizedEvent, keywords: tuple[str, ...]) -> bool:
    haystack = f"{event.action} {event.raw_message}".lower()
    return any(keyword in haystack for keyword in keywords)


def _format_evidence(event: NormalizedEvent) -> str:
    timestamp = event.timestamp.isoformat() if event.timestamp else "unknown time"
    return (
        f"{timestamp} | source={event.source} host={event.host} "
        f"user={event.user} action={event.action}"
    )


def _title_for_phase(phase: str, event: NormalizedEvent) -> str:
    host = event.host if event.host != "unknown" else "affected asset"
    return f"{phase} activity observed on {host}"


def _inference_for_phase(phase: str) -> str:
    return {
        "Initial Access": (
            "A successful authentication or trusted-account event may indicate the entry point."
        ),
        "Credential Access": (
            "Repeated authentication failures suggest credential guessing or password spraying."
        ),
        "Execution": "Suspicious command execution indicates payload or script activity.",
        "Lateral Movement": "Administrative share or SMB activity suggests movement between hosts.",
        "Command and Control": "Beacon-like or C2-labeled traffic suggests external coordination.",
        "Impact": "Encryption or ransom indicators suggest business-impacting activity.",
    }[phase]
