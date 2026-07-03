import json
from collections import Counter
from pathlib import Path

from app.schemas import ExecutionResult, QueryJob
from app.services.intent import department_filter, detect_intents

ROOT = Path(__file__).resolve().parents[3]
SAMPLE_EVENTS = ROOT / "sample-data" / "events" / "security-events.jsonl"


def execute_against_sample(job: QueryJob) -> ExecutionResult:
    events = _load_events()
    intents = detect_intents(job.question)
    department = department_filter(job.question)
    action_terms = {term for intent in intents for term in intent.action_terms}
    wants_foreign = any(intent.name == "foreign_outbound" for intent in intents)

    matched = []
    for event in events:
        if event.get("action") not in action_terms:
            continue
        if wants_foreign and event.get("country") == "VN":
            continue
        if department and event.get("department") != department:
            continue
        matched.append(event)

    grouped = _group_rows(matched)
    return ExecutionResult(
        row_count=len(grouped),
        rows=grouped[:50],
        summary=_summary(matched, grouped),
    )


def _load_events() -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    for line in SAMPLE_EVENTS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def _group_rows(events: list[dict[str, str]]) -> list[dict[str, str]]:
    counter: Counter[tuple[str, str, str, str, str, str, str]] = Counter()
    first_seen: dict[tuple[str, str, str, str, str, str, str], str] = {}
    last_seen: dict[tuple[str, str, str, str, str, str, str], str] = {}
    for event in events:
        key = (
            event.get("host", ""),
            event.get("user", ""),
            event.get("src_ip", ""),
            event.get("dst_ip", ""),
            event.get("country", ""),
            event.get("action", ""),
            event.get("severity", ""),
        )
        counter[key] += 1
        timestamp = event.get("timestamp", "")
        first_seen[key] = min(first_seen.get(key, timestamp), timestamp)
        last_seen[key] = max(last_seen.get(key, timestamp), timestamp)

    rows = []
    for key, count in counter.most_common():
        host, user, src_ip, dst_ip, country, action, severity = key
        rows.append(
            {
                "count": str(count),
                "first_seen": first_seen[key],
                "last_seen": last_seen[key],
                "host": host,
                "user": user,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "country": country,
                "action": action,
                "severity": severity,
            }
        )
    return rows


def _summary(events: list[dict[str, str]], rows: list[dict[str, str]]) -> str:
    if not events:
        return "No matching events were found in the synthetic dataset."
    host_count = len({event.get("host", "") for event in events})
    user_count = len({event.get("user", "") for event in events if event.get("user")})
    return (
        f"Matched {len(events)} raw events grouped into {len(rows)} result rows "
        f"across {host_count} hosts and {user_count} users."
    )
