from typing import Sequence

from fastapi import HTTPException, status

from app.core.security import get_hash_password, verify_password
from app.models.user import User
from app.respositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """
    Service layer for user business logic.
    Orchestrates operations between controllers and repositories.
    Does not know about Client layer - receives Repository directly.
    """

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, user_create: UserCreate) -> User:
        existing = self.repo.get_by_email(user_create.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        hashed = get_hash_password(user_create.password)
        user = self.repo.create(user_create=user_create, hashed_password=hashed)
        return user

    def list_users(self, limit: int = 100, offset: int = 0) -> Sequence[User]:
        return self.repo.list(limit=limit, offset=offset)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Authenticate a user by email and password

        Args:
            email: User's email address
            password: Plain text password to verify

        Returns:
            User object if credentials are valid, None otherwise
        """

        user = self.repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
