import pytest
from sqlalchemy import text
from sqlmodel import SQLModel, Session

from app.db.database import test_postgres_client


@pytest.fixture(scope="session")
def setup_test_db():
    """
    Create all tables in test database at session start.
    Runs once per test session.
    """
    test_postgres_client.create_tables(SQLModel.metadata)
    yield
    # Cleanup after all tests - drop all tables in reverse order
    with test_postgres_client.get_session_context() as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.query(table).delete()
        session.commit()
        # Drop tables
        SQLModel.metadata.drop_all(test_postgres_client.engine)


@pytest.fixture
def db_session(setup_test_db):
    """
    Provide a clean database session for each test.
    Rolls back all changes after test completes for test isolation.
    """
    session = next(test_postgres_client.get_session())
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def test_client():
    """
    Provide test postgres client instance for direct repository testing.
    """
    return test_postgres_client
