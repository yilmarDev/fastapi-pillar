from typing import Sequence
from fastapi import HTTPException, status
from app.models.user import User
from app.respositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_hash_password


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
