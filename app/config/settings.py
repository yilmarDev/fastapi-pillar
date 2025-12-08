from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")  # type: ignore[arg-type]

    env: str = Field(default="development", validation_alias="ENV")
    database_url: str = Field(default="", validation_alias="DATABASE_URL")
    test_database_url: str = Field(default="", validation_alias="TEST_DATABASE_URL")


@lru_cache()
def get_settings():
    return Settings()
