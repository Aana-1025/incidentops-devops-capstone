"""Environment-based application settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    app_name: str = "IncidentOps API"
    app_env: str = "development"
    database_url: str = (
        "postgresql+psycopg://incidentops:incidentops@localhost:5432/incidentops"
    )
    database_connect_timeout_seconds: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings object for the process."""

    return Settings()


settings = get_settings()
