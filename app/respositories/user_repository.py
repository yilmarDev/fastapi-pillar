from typing import Sequence
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select


from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
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
        return self.session.get(User, user_id)

    def get_by_email(self, email: EmailStr) -> User | None:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def list(self, limit: int = 100, offset: int = 0) -> Sequence[User]:
        statement = select(User).limit(limit).offset(offset)
        return self.session.exec(statement).all()

    def update(self, user: User, **kwargs) -> User:
        for k, v in kwargs.items():
            setattr(user, k, v)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
