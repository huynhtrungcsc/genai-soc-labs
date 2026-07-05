import base64
import json
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8003/api"
AUTH = base64.b64encode(b"analyst:threatpulse-demo").decode()


def request(path: str, method: str = "GET", payload: dict[str, object] | None = None) -> object:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Basic {AUTH}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode())


def main() -> None:
    health = urllib.request.urlopen(f"{BASE_URL}/health", timeout=10).read().decode()
    ready = urllib.request.urlopen(f"{BASE_URL}/ready", timeout=10).read().decode()
    intel = request("/intel")
    briefing = request(
        "/briefings/generate",
        method="POST",
        payload={"audience": "soc", "lookback_days": 30, "max_items": 5},
    )
    approved = request(
        f"/briefings/{briefing['id']}/approve",
        method="POST",
        payload={"approver": "soc-manager", "note": "Smoke test approval"},
    )

    print(health)
    print(ready)
    print(f"intel_items={len(intel)}")
    print(f"briefing_sections={len(briefing['sections'])}")
    print(f"approval_status={approved['status']}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as exc:
        raise SystemExit(f"Smoke test failed: {exc}") from exc
