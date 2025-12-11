from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")  # type: ignore[arg-type]

    env: str = Field(default="development", validation_alias="ENV")
    test_database_url: str = Field(default="", validation_alias="TEST_DATABASE_URL")

    @property
    def database_url(self) -> str:
        # Try formatted URL first, then convert legacy format
        formatted = os.getenv("DATABASE_URL_FORMATTED")
        if formatted:
            return formatted

        legacy = os.getenv("DATABASE_URL", "")
        if legacy:
            # Convert postgres:// to postgresql+psycopg://
            return legacy.replace("postgres://", "postgresql+psycopg://", 1)

        return ""


@lru_cache()
def get_settings():
    return Settings()
