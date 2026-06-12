from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.docker", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = Field(default="development", validation_alias="ENV")
    database_url: str = Field(default="", validation_alias="DATABASE_URL")
    test_database_url: str = Field(default="", validation_alias="TEST_DATABASE_URL")
    secret_key: str = Field(
        default="dev-secret-key-change-in-production", validation_alias="SECRET_KEY"
    )
    algorithm: str = Field(default="", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    @field_validator("database_url", mode="after")
    @classmethod
    def convert_postgres_url(cls, v: str) -> str:
        """Convert legacy postgres:// URLs to postgresql+psycopg:// format"""
        if v:
            return v.replace("postgres://", "postgresql+psycopg://", 1)
        return v


@lru_cache()
def get_settings():
    return Settings()
