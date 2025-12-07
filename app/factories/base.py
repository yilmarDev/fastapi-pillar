from factory.alchemy import SQLAlchemyModelFactory
from sqlmodel import Session
from app.db.database import postgres_client, test_postgres_client
from app.config.settings import get_settings


settings = get_settings()


def get_factory_client():
    """
    Returns the appropriate PostgreSQL client based on environment.
    - test: uses test_postgres_client
    - development/production: uses postgres_client (real DB)
    """
    if settings.env == "test":
        return test_postgres_client
    return postgres_client


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session(get_factory_client().engine)
        sqlalchemy_session_persistence = "commit"
