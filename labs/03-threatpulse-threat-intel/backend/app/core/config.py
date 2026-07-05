from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ThreatPulse"
    database_path: Path = Path("data/threatpulse.sqlite3")
    api_key: str = Field(default="change-me-in-production", validation_alias="THREATPULSE_API_KEY")
    demo_username: str = Field(default="analyst", validation_alias="THREATPULSE_DEMO_USERNAME")
    demo_password: str = Field(
        default="threatpulse-demo",
        validation_alias="THREATPULSE_DEMO_PASSWORD",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
