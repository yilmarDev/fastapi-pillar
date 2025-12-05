from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    env: str = "development"
    database_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
