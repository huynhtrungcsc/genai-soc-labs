from functools import lru_cache
from os import getenv
from pathlib import Path


class Settings:
    app_name: str = getenv("QUERYFORGE_APP_NAME", "QueryForge")
    environment: str = getenv("QUERYFORGE_ENV", "development")
    database_path: Path = Path(getenv("QUERYFORGE_DATABASE_PATH", "./data/queryforge.db"))
    demo_username: str = getenv("QUERYFORGE_DEMO_USERNAME", "hunter")
    demo_password: str = getenv("QUERYFORGE_DEMO_PASSWORD", "queryforge-demo")
    api_key: str = getenv("QUERYFORGE_API_KEY", "change-me-in-production")


@lru_cache
def get_settings() -> Settings:
    return Settings()
