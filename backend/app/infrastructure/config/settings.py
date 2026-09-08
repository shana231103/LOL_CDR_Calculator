# File: backend/app/infrastructure/config/settings.py

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings loaded from environment variables or .env file."""

    app_name: str = "LoL Cooldown Calculator API"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # Database: Supports asyncpg PostgreSQL and aiosqlite SQLite
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cdr_lol"

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*",
    ]

    # Riot Data Dragon CDN
    riot_ddragon_cdn: str = "https://ddragon.leagueoflegends.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
