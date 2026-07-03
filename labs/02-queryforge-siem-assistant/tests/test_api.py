import base64
import os

os.environ["QUERYFORGE_DATABASE_PATH"] = "./data/test-queryforge.db"

from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


def _auth() -> dict[str, str]:
    token = base64.b64encode(b"hunter:queryforge-demo").decode()
    return {"Authorization": f"Basic {token}"}


def _api_key() -> dict[str, str]:
    return {"X-API-Key": "change-me-in-production"}


def test_query_workflow() -> None:
    with TestClient(app) as client:
        health = client.get("/api/health")
        assert health.status_code == 200

        unauthenticated = client.get("/api/queries")
        assert unauthenticated.status_code == 401

        created = client.post(
            "/api/queries",
            headers=_auth(),
            json={
                "question": "Có máy nào trong phòng kế toán kết nối ra IP lạ ở nước ngoài không?",
                "dialect": "splunk",
                "time_range": "24h",
                "data_source": "security_events",
            },
        )
        assert created.status_code == 201
        job = created.json()
        assert 'country!="VN"' in job["generated"]["query"]
        assert job["status"] == "draft"

        executed = client.post(f"/api/queries/{job['id']}/execute", headers=_auth())
        assert executed.status_code == 409

        approved = client.post(
            f"/api/queries/{job['id']}/approve",
            headers=_auth(),
            json={"approver": "soc-lead", "note": "Reviewed in test workflow."},
        )
        assert approved.status_code == 200
        assert approved.json()["status"] == "approved"

        executed = client.post(f"/api/queries/{job['id']}/execute", headers=_auth())
        assert executed.status_code == 200
        assert executed.json()["execution"]["row_count"] >= 2

        audit = client.get(f"/api/queries/{job['id']}/audit", headers=_api_key())
        assert audit.status_code == 200
        actions = {item["action"] for item in audit.json()}
        assert {"query.created", "query.approved", "query.executed"} <= actions
