from pathlib import Path

from app.schemas import Incident, IncidentCreate
from app.services.analysis import analyze_incident

SAMPLE = Path("sample-data/incidents/acme-ransomware/logs.jsonl")


def test_analysis_builds_timeline_mitre_and_reports() -> None:
    payload = IncidentCreate(
        title="ACME ransomware intrusion",
        severity="high",
        summary="Synthetic incident",
        raw_logs=SAMPLE.read_text(encoding="utf-8"),
    )
    incident = Incident(
        id="test",
        title=payload.title,
        severity=payload.severity,
        summary=payload.summary,
        raw_logs=payload.raw_logs,
        created_at="2026-06-28T00:00:00+00:00",
        updated_at="2026-06-28T00:00:00+00:00",
    )

    analyzed = analyze_incident(incident)

    assert len(analyzed.events) == 7
    assert {step.phase for step in analyzed.timeline} >= {
        "Credential Access",
        "Execution",
        "Impact",
    }
    assert {item.technique_id for item in analyzed.mitre} >= {"T1110", "T1059.001", "T1486"}
    assert analyzed.reports is not None
    assert "Technical Incident Report" in analyzed.reports.technical
    assert "Executive Brief" in analyzed.reports.executive
