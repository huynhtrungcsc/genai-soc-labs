from app.services.parser import parse_logs


def test_parse_jsonl_logs_extracts_core_fields() -> None:
    raw = (
        '{"timestamp":"2026-06-28T08:24:11Z","source":"edr","host":"FIN-WS-044",'
        '"user":"j.nguyen","action":"suspicious_powershell",'
        '"message":"powershell.exe -EncodedCommand detected"}'
    )

    events = parse_logs(raw)

    assert len(events) == 1
    assert events[0].source == "edr"
    assert events[0].host == "FIN-WS-044"
    assert events[0].user == "j.nguyen"
    assert events[0].action == "suspicious_powershell"


def test_parse_text_logs_infers_action_and_ips() -> None:
    raw = "2026-06-28T08:52:03Z source=zeek host=FIN-WS-044 C2 beacon 10.0.0.4 198.51.100.77"

    events = parse_logs(raw)

    assert events[0].action == "command_and_control"
    assert events[0].src_ip == "10.0.0.4"
    assert events[0].dst_ip == "198.51.100.77"
