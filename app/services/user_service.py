from sqlmodel import Session

from app.respositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def register_user(self, user_create: UserCreate):
        existing = self.repo.get_by_email(user_create.email)
        if existing:
            raise ValueError("Email already registered")

        hashed = hash_password(user_create.password)
        user = self.repo.create(user_create=user_create, hashed_password=hashed)
        return user

    def list_users(self, limit: int = 100, offtset: int = 0):
        return self.repo.list(limit=limit, offset=offtset)
