from dataclasses import dataclass

from app.schemas import MitreTechnique, NormalizedEvent


@dataclass(frozen=True)
class Rule:
    keywords: tuple[str, ...]
    tactic: str
    technique_id: str
    technique: str
    confidence: float


RULES = (
    Rule(
        ("failed_login", "brute force", "password spray"),
        "Credential Access",
        "T1110",
        "Brute Force",
        0.82,
    ),
    Rule(
        ("successful_login", "vpn login", "new device"),
        "Initial Access",
        "T1078",
        "Valid Accounts",
        0.74,
    ),
    Rule(
        ("powershell", "encodedcommand", "downloadstring"),
        "Execution",
        "T1059.001",
        "PowerShell",
        0.86,
    ),
    Rule(
        ("admin$", "smb", "psexec"),
        "Lateral Movement",
        "T1021.002",
        "SMB/Windows Admin Shares",
        0.8,
    ),
    Rule(
        ("beacon", "c2", "command_and_control"),
        "Command and Control",
        "T1071",
        "Application Layer Protocol",
        0.72,
    ),
    Rule(
        ("ransom", "encrypt", "encrypted"),
        "Impact",
        "T1486",
        "Data Encrypted for Impact",
        0.88,
    ),
)


def map_to_mitre(events: list[NormalizedEvent]) -> list[MitreTechnique]:
    mapped: dict[str, MitreTechnique] = {}
    for event in events:
        haystack = f"{event.action} {event.raw_message}".lower()
        for rule in RULES:
            if any(keyword in haystack for keyword in rule.keywords):
                existing = mapped.get(rule.technique_id)
                evidence = _evidence(event)
                if existing:
                    if evidence not in existing.evidence:
                        existing.evidence.append(evidence)
                else:
                    mapped[rule.technique_id] = MitreTechnique(
                        tactic=rule.tactic,
                        technique_id=rule.technique_id,
                        technique=rule.technique,
                        evidence=[evidence],
                        confidence=rule.confidence,
                    )
    return list(mapped.values())


def _evidence(event: NormalizedEvent) -> str:
    timestamp = event.timestamp.isoformat() if event.timestamp else "unknown time"
    return f"{timestamp} | {event.host} | {event.user} | {event.action}: {event.raw_message}"
