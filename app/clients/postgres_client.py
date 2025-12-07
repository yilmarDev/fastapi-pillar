from sqlmodel import create_engine, Session
from typing import Generator


class PostgresClient:
    """
    PostgreSQL database client responsible for managing database connections
    and providing session instances for data access operations.
    """

    def __init__(self, database_url: str, echo: bool = False):
        """
        Initialize the PostgreSQL client with a database connection.

        Args:
            database_url: PostgreSQL connection string
            echo: If True, SQL statements will be logged (useful for debugging)
        """
        self.database_url = database_url
        self.engine = create_engine(
            database_url,
            echo=echo,
            pool_pre_ping=True,
        )

    def get_session(self) -> Generator[Session, None, None]:
        """
        Create and yield a database session.

        Yields:
            Session: SQLModel session for database operations
        """
        with Session(self.engine) as session:
            yield session

    def create_tables(self, metadata) -> None:
        """
        Create all tables defined in the metadata.

        Args:
            metadata: SQLModel metadata containing table definitions
        """
        metadata.create_all(self.engine)

    def close(self) -> None:
        """
        Close the database engine and all its connections.
        """
        self.engine.dispose()
