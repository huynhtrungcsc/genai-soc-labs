from functools import lru_cache
from os import getenv
from pathlib import Path


class Settings:
    app_name: str = getenv("INCIDENTLENS_APP_NAME", "IncidentLens")
    environment: str = getenv("INCIDENTLENS_ENV", "development")
    database_path: Path = Path(getenv("INCIDENTLENS_DATABASE_PATH", "./data/incidentlens.db"))
    demo_username: str = getenv("INCIDENTLENS_DEMO_USERNAME", "analyst")
    demo_password: str = getenv("INCIDENTLENS_DEMO_PASSWORD", "incidentlens-demo")


@lru_cache
def get_settings() -> Settings:
    return Settings()
