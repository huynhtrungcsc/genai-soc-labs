import base64
import os

os.environ["QUERYFORGE_DATABASE_PATH"] = "./data/test-queryforge.db"

from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


def _auth() -> dict[str, str]:
    token = base64.b64encode(b"hunter:queryforge-demo").decode()
    return {"Authorization": f"Basic {token}"}


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

        executed = client.post(f"/api/queries/{job['id']}/execute", headers=_auth())
        assert executed.status_code == 200
        assert executed.json()["execution"]["row_count"] >= 2
