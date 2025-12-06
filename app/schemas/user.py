from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool

    class Config:
        orm_mode = True


class userUpdate(BaseModel):
    full_name: str | None
    is_active: str | None
