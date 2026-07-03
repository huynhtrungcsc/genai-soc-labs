from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    name: str
    action_terms: tuple[str, ...]
    explanation: str
    next_questions: tuple[str, ...]


INTENTS = (
    Intent(
        name="failed_login",
        action_terms=("failed_login", "login_failed"),
        explanation="Find authentication failures that may indicate password spraying.",
        next_questions=(
            "Which accounts had a successful login after repeated failures?",
            "Are the source IPs new for the affected users?",
        ),
    ),
    Intent(
        name="suspicious_powershell",
        action_terms=("suspicious_powershell", "powershell"),
        explanation="Find suspicious PowerShell or encoded command execution.",
        next_questions=(
            "Which parent process launched PowerShell?",
            "Did the host connect to an external IP after execution?",
        ),
    ),
    Intent(
        name="foreign_outbound",
        action_terms=("outbound_connection", "network_connection"),
        explanation="Find outbound network connections to non-Vietnam destinations.",
        next_questions=(
            "Which destination countries are unusual for this department?",
            "Did any outbound connection happen after a suspicious process event?",
        ),
    ),
    Intent(
        name="lateral_movement",
        action_terms=("lateral_movement", "smb_admin_share"),
        explanation="Find SMB or administrative share activity that may indicate lateral movement.",
        next_questions=(
            "Were privileged accounts used for these connections?",
            "Which hosts saw both source and destination activity?",
        ),
    ),
    Intent(
        name="c2_beacon",
        action_terms=("command_and_control", "beacon"),
        explanation="Find beacon-like C2 activity from internal hosts.",
        next_questions=(
            "Is the beacon interval regular across multiple hours?",
            "Do other hosts communicate with the same destination?",
        ),
    ),
)


def detect_intents(question: str) -> list[Intent]:
    text = question.lower()
    matches: list[Intent] = []
    if any(term in text for term in ("failed", "thất bại", "brute", "spray", "đăng nhập sai")):
        matches.append(INTENTS[0])
    if any(term in text for term in ("powershell", "encoded", "script", "lệnh")):
        matches.append(INTENTS[1])
    if any(term in text for term in ("foreign", "nước ngoài", "outbound", "kết nối ra", "ip lạ")):
        matches.append(INTENTS[2])
    if any(term in text for term in ("smb", "admin$", "lateral", "di chuyển ngang")):
        matches.append(INTENTS[3])
    if any(term in text for term in ("c2", "beacon", "command and control", "gọi về")):
        matches.append(INTENTS[4])
    return matches or [INTENTS[2]]


def department_filter(question: str) -> str | None:
    text = question.lower()
    if any(term in text for term in ("kế toán", "accounting", "finance", "tài chính")):
        return "finance"
    if any(term in text for term in ("hr", "nhân sự")):
        return "hr"
    if any(term in text for term in ("it", "infrastructure", "hạ tầng")):
        return "it"
    return None
