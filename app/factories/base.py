from factory.alchemy import SQLAlchemyModelFactory
from sqlmodel import Session
from app.db.database import engine, test_engine
from app.config.settings import get_settings


settings = get_settings()


def get_factory_engine():
    """
    Retorna el engine apropiado según el entorno.
    - test: usa test_engine
    - development/production: usa engine (DB real)
    """
    if settings.env == "test":
        return test_engine
    return engine


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session(get_factory_engine())
        sqlalchemy_session_persistence = "commit"
