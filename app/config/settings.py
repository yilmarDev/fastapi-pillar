from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, field_validator
from functools import lru_cache


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")  # type: ignore[arg-type]

    env: str = Field(default="development", validation_alias="ENV")
    database_url: str = Field(default="", validation_alias="DATABASE_URL")
    test_database_url: str = Field(default="", validation_alias="TEST_DATABASE_URL")

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
