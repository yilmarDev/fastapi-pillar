from sqlmodel import SQLModel, create_engine, Session
from app.config.settings import get_settings

settings = get_settings()


def get_engine(test: bool = False):
    database_url = settings.test_database_url if test else settings.database_url

    # echo=Ture only for debug SQL, change to False in prod
    engine = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
    )
    return engine


# App and test motors
engine = get_engine(test=False)
test_engine = get_engine(test=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency injection para FastAPI.
    Crea una sesión nueva por request.
    """
    with Session(engine) as session:
        yield session
