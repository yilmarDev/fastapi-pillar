from sqlmodel import SQLModel
from app.config.settings import get_settings
from app.clients.postgres_client import PostgresClient

settings = get_settings()

# PostgreSQL clients for app and tests
postgres_client = PostgresClient(database_url=settings.database_url, echo=False)

# Only create test client if TEST_DATABASE_URL is configured
test_postgres_client = None
if settings.test_database_url:
    test_postgres_client = PostgresClient(
        database_url=settings.test_database_url, echo=False
    )


def create_db_and_tables() -> None:
    """
    Create all database tables using SQLModel metadata.
    """
    postgres_client.create_tables(SQLModel.metadata)


def get_postgres_client() -> PostgresClient:
    """
    Dependency injection for FastAPI.
    Returns the main PostgreSQL client instance.
    """
    return postgres_client


def get_test_postgres_client() -> PostgresClient:
    """
    Dependency injection for tests.
    Returns the test PostgreSQL client instance.
    """
    return test_postgres_client
