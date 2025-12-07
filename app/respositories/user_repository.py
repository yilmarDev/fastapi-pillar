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
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
        )

        session_gen = self.client.get_session()
        session = next(session_gen)
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    def get_by_id(self, user_id: UUID) -> User | None:
        session_gen = self.client.get_session()
        session = next(session_gen)
        try:
            return session.get(User, user_id)
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    def get_by_email(self, email: EmailStr) -> User | None:
        session_gen = self.client.get_session()
        session = next(session_gen)
        try:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    def list(self, limit: int = 100, offset: int = 0) -> Sequence[User]:
        session_gen = self.client.get_session()
        session = next(session_gen)
        try:
            statement = select(User).limit(limit).offset(offset)
            return session.exec(statement).all()
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    def update(self, user: User, **kwargs) -> User:
        session_gen = self.client.get_session()
        session = next(session_gen)
        try:
            for k, v in kwargs.items():
                setattr(user, k, v)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass

    def delete(self, user: User) -> None:
        session_gen = self.client.get_session()
        session = next(session_gen)
        try:
            session.delete(user)
            session.commit()
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass
