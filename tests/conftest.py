import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.routers.users import router
from app.db.database import test_postgres_client
from app.dependencies.user_dependencies import get_db


@pytest.fixture(scope="session", autouse=True)
def print_test_db_info():
    """
    Print test database URL
    """
    print(f"\n\n{'='*70}")
    print(f"Test url BD: ", test_postgres_client.engine.url)
    print(f"\n{'='*70}")
    yield


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


@pytest.fixture
def app(db_session):
    """
    Provide a FastAPI app with routers for testing.
    Override get_db dependency to use test session.
    """
    app = FastAPI()
    app.include_router(router)

    # Override get_db to return the test session as a generator
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    """Provide a TestClient instance for API endpoint testing"""
    return TestClient(app)
