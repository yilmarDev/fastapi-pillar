from typing import Sequence
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    """
    Repository for User data access operations.
    Receives a database session for all operations.
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        """Create a new user with hashed password."""
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve user by ID."""
        return self.session.get(User, user_id)

    def get_by_email(self, email: EmailStr) -> User | None:
        """Retrieve user by email address."""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def list(self, limit: int = 100, offset: int = 0) -> Sequence[User]:
        """List users with pagination."""
        statement = select(User).limit(limit).offset(offset)
        return self.session.exec(statement).all()

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
