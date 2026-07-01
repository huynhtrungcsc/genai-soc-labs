import base64
import os
from pathlib import Path

os.environ["INCIDENTLENS_DATABASE_PATH"] = "./data/test-incidentlens.db"

from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

SAMPLE = Path("sample-data/incidents/acme-ransomware/logs.jsonl")


def _auth() -> dict[str, str]:
    token = base64.b64encode(b"analyst:incidentlens-demo").decode()
    return {"Authorization": f"Basic {token}"}


def test_incident_workflow() -> None:
    with TestClient(app) as client:
        health = client.get("/api/health")
        assert health.status_code == 200

        unauthenticated = client.get("/api/incidents")
        assert unauthenticated.status_code == 401

        created = client.post(
            "/api/incidents",
            headers=_auth(),
            json={
                "title": "ACME ransomware intrusion",
                "severity": "high",
                "summary": "Synthetic incident",
                "raw_logs": SAMPLE.read_text(encoding="utf-8"),
            },
        )
        assert created.status_code == 201
        incident = created.json()
        assert len(incident["events"]) == 7

        report = client.get(f"/api/incidents/{incident['id']}/report/technical", headers=_auth())
        assert report.status_code == 200
        assert "Technical Incident Report" in report.text
