from typing import Sequence
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.clients.postgres_client import PostgresClient


class UserRepository:
    """
    Repository for User data access operations.
    Uses PostgresClient to abstract database connection details.
    """

    def __init__(self, client: PostgresClient):
        self.client = client

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        """Create a new user with hashed password."""
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
        )

        with self.client.get_session_context() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve user by ID."""
        with self.client.get_session_context() as session:
            return session.get(User, user_id)

    def get_by_email(self, email: EmailStr) -> User | None:
        """Retrieve user by email address."""
        with self.client.get_session_context() as session:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()

    def list(self, limit: int = 100, offset: int = 0) -> Sequence[User]:
        """List users with pagination."""
        with self.client.get_session_context() as session:
            statement = select(User).limit(limit).offset(offset)
            return session.exec(statement).all()

    def update(self, user: User, **kwargs) -> User:
        """Update user with given attributes."""
        with self.client.get_session_context() as session:
            for k, v in kwargs.items():
                setattr(user, k, v)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def delete(self, user: User) -> None:
        """Delete a user."""
        with self.client.get_session_context() as session:
            session.delete(user)
            session.commit()
