from uuid import uuid4, UUID
from datetime import datetime

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, DateTime, func


class UserBase(SQLModel):
    email: str = Field(
        sa_column=Column(String, nullable=False, unique=True, index=True)
    )
    full_name: str | None = Field(default=None)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    create_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    update_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )
