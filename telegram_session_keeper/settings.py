from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    log_level: str = "INFO"

    api_id: int
    api_hash: str

    db_path: Path = Path("db.csv")

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")


settings = Settings()
