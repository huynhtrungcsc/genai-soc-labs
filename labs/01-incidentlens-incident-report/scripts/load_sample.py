from pathlib import Path

from app.schemas import IncidentCreate
from app.services.analysis import analyze_incident
from app.storage.sqlite import create_incident, init_db, save_incident

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample-data" / "incidents" / "acme-ransomware" / "logs.jsonl"


def main() -> None:
    init_db()
    incident = create_incident(
        IncidentCreate(
            title="ACME ransomware intrusion",
            severity="high",
            summary="Synthetic intrusion scenario for validating IncidentLens workflow.",
            raw_logs=SAMPLE.read_text(encoding="utf-8"),
        )
    )
    save_incident(analyze_incident(incident))
    print(f"Loaded sample incident: {incident.id}")


if __name__ == "__main__":
    main()
