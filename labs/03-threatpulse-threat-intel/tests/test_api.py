import os
from pathlib import Path

from fastapi.testclient import TestClient

os.environ["THREATPULSE_API_KEY"] = "test-key"
os.environ["THREATPULSE_DEMO_USERNAME"] = "analyst"
os.environ["THREATPULSE_DEMO_PASSWORD"] = "threatpulse-demo"
os.environ["DATABASE_PATH"] = str(Path("data/test-threatpulse.sqlite3"))

from app.core.config import get_settings  # noqa: E402
from app.main import create_app  # noqa: E402

get_settings.cache_clear()

AUTH = ("analyst", "threatpulse-demo")


def client() -> TestClient:
    db_path = Path("data/test-threatpulse.sqlite3")
    if db_path.exists():
        db_path.unlink()
    return TestClient(create_app())


def test_health_is_public() -> None:
    with client() as test_client:
        response = test_client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["service"] == "threatpulse"


def test_full_threat_intel_workflow() -> None:
    with client() as test_client:
        asset_response = test_client.post(
            "/api/assets",
            auth=AUTH,
            json={
                "hostname": "vpn-edge-01",
                "owner": "network-security",
                "business_unit": "infrastructure",
                "environment": "production",
                "criticality": 5,
                "technologies": ["Ivanti Connect Secure", "Linux"],
                "internet_exposed": True,
                "data_classification": "internal",
                "tags": ["edge"],
            },
        )
        assert asset_response.status_code == 201

        intel_response = test_client.post(
            "/api/intel",
            auth=AUTH,
            json={
                "source": "CISA KEV",
                "title": (
                    "Active exploitation reported for Ivanti Connect Secure "
                    "gateway vulnerability"
                ),
                "summary": "Threat report describes exploitation of exposed appliances.",
                "affected_products": ["Ivanti Connect Secure"],
                "industries": ["financial-services"],
                "cves": ["CVE-2025-0282"],
                "iocs": ["198.51.100.77"],
                "mitre_techniques": ["T1190"],
                "references": ["https://www.cisa.gov/known-exploited-vulnerabilities-catalog"],
                "observed_exploitation": True,
                "severity": "critical",
                "confidence": "high",
                "source_reliability": "A",
                "published_at": "2026-07-01T09:30:00+00:00",
            },
        )
        assert intel_response.status_code == 201
        intel = intel_response.json()
        assert intel["assessment"]["priority"] == "critical"
        assert intel["assessment"]["affected_assets"][0]["hostname"] == "vpn-edge-01"

        briefing_response = test_client.post(
            "/api/briefings/generate",
            auth=AUTH,
            json={"audience": "soc", "lookback_days": 30, "max_items": 5},
        )
        assert briefing_response.status_code == 201
        briefing = briefing_response.json()
        assert briefing["status"] == "draft"
        assert briefing["sections"]

        approval_response = test_client.post(
            f"/api/briefings/{briefing['id']}/approve",
            auth=AUTH,
            json={"approver": "soc-manager", "note": "Reviewed"},
        )
        assert approval_response.status_code == 200
        assert approval_response.json()["status"] == "approved"

        audit_response = test_client.get("/api/audit", auth=AUTH)
        assert audit_response.status_code == 200
        assert len(audit_response.json()) >= 4


def test_protected_endpoint_requires_auth() -> None:
    with client() as test_client:
        response = test_client.get("/api/assets")

    assert response.status_code == 401


def test_reassess_updates_intel_after_inventory_change() -> None:
    with client() as test_client:
        intel_response = test_client.post(
            "/api/intel",
            auth=AUTH,
            json={
                "source": "Vendor Advisory",
                "title": "MOVEit Transfer patch advisory for managed file transfer deployments",
                "summary": "Vendor advisory describes a managed file transfer vulnerability.",
                "affected_products": ["MOVEit Transfer"],
                "industries": ["financial-services"],
                "cves": ["CVE-2026-41001"],
                "iocs": ["203.0.113.44"],
                "mitre_techniques": ["T1190"],
                "references": ["https://example.com/vendor/moveit-advisory"],
                "observed_exploitation": False,
                "severity": "high",
                "confidence": "medium",
                "source_reliability": "B",
                "published_at": "2026-07-02T15:10:00+00:00",
            },
        )
        assert intel_response.status_code == 201
        assert intel_response.json()["assessment"]["affected_assets"] == []

        test_client.post(
            "/api/assets",
            auth=AUTH,
            json={
                "hostname": "crm-app-03",
                "owner": "customer-operations",
                "business_unit": "operations",
                "environment": "production",
                "criticality": 4,
                "technologies": ["MOVEit Transfer", "Windows Server"],
                "internet_exposed": False,
                "data_classification": "confidential",
                "tags": ["customer-data"],
            },
        )

        reassess_response = test_client.post("/api/intel/reassess", auth=AUTH)
        assert reassess_response.status_code == 200
        reassessed = reassess_response.json()[0]
        assert reassessed["assessment"]["affected_assets"][0]["hostname"] == "crm-app-03"
