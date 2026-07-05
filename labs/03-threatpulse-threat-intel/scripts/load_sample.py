import json
from pathlib import Path

from app.schemas import AssetRequest, IntelRequest
from app.storage.sqlite import create_asset, create_intel_item, init_db, record_audit

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    init_db()
    assets = [
        create_asset(AssetRequest.model_validate(item))
        for item in load_json(ROOT / "sample-data" / "assets" / "assets.json")
    ]
    intel = [
        create_intel_item(IntelRequest.model_validate(item))
        for item in load_json(ROOT / "sample-data" / "intel" / "threat-intel.json")
    ]
    record_audit(
        "seed-script",
        "sample.loaded",
        "sample-data",
        f"Loaded {len(assets)} assets and {len(intel)} intelligence items",
    )
    print(f"Loaded {len(assets)} assets and {len(intel)} intelligence items")


if __name__ == "__main__":
    main()
