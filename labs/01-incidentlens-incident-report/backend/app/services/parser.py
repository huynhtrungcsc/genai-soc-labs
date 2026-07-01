import json
import re
from datetime import datetime

from app.schemas import NormalizedEvent

ISO_TS = re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})?)")
IP = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
KEY_VALUE = re.compile(r"(?P<key>host|user|src_ip|dst_ip|source|action)=(?P<value>[^\s,]+)")


def parse_logs(raw_logs: str) -> list[NormalizedEvent]:
    events: list[NormalizedEvent] = []
    for line in raw_logs.splitlines():
        line = line.strip()
        if not line:
            continue
        events.append(_parse_json_line(line) or _parse_text_line(line))
    return sorted(
        events,
        key=lambda event: (
            event.timestamp is None,
            event.timestamp.isoformat() if event.timestamp else "",
        ),
    )


def _parse_json_line(line: str) -> NormalizedEvent | None:
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return None

    message = str(payload.get("message") or payload.get("raw_message") or line)
    ips = IP.findall(message)
    return NormalizedEvent(
        timestamp=_parse_timestamp(payload.get("timestamp") or payload.get("@timestamp")),
        source=str(payload.get("source") or payload.get("event_source") or "json"),
        host=str(payload.get("host") or payload.get("hostname") or "unknown"),
        user=str(payload.get("user") or payload.get("username") or "unknown"),
        action=str(payload.get("action") or payload.get("event") or _infer_action(message)),
        src_ip=payload.get("src_ip") or payload.get("source_ip") or (ips[0] if ips else None),
        dst_ip=(
            payload.get("dst_ip")
            or payload.get("destination_ip")
            or (ips[1] if len(ips) > 1 else None)
        ),
        raw_message=message,
    )


def _parse_text_line(line: str) -> NormalizedEvent:
    fields = {match.group("key"): match.group("value") for match in KEY_VALUE.finditer(line)}
    ips = IP.findall(line)
    ts_match = ISO_TS.search(line)
    timestamp = _parse_timestamp(ts_match.group("ts")) if ts_match else None
    return NormalizedEvent(
        timestamp=timestamp,
        source=fields.get("source", "text"),
        host=fields.get("host", "unknown"),
        user=fields.get("user", "unknown"),
        action=fields.get("action", _infer_action(line)),
        src_ip=fields.get("src_ip") or (ips[0] if ips else None),
        dst_ip=fields.get("dst_ip") or (ips[1] if len(ips) > 1 else None),
        raw_message=line,
    )


def _parse_timestamp(value: object) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _infer_action(message: str) -> str:
    text = message.lower()
    if "failed" in text and ("login" in text or "logon" in text):
        return "failed_login"
    if "success" in text and ("login" in text or "logon" in text):
        return "successful_login"
    if "powershell" in text or "encodedcommand" in text:
        return "suspicious_powershell"
    if "smb" in text or "admin$" in text:
        return "lateral_movement"
    if "encrypt" in text or "ransom" in text:
        return "impact"
    if "dns" in text or "beacon" in text or "c2" in text:
        return "command_and_control"
    return "observed"
