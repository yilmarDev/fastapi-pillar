from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=8, description="Min 8 characters")
    full_name: str | None = Field(None, min_length=4, description="Full name")


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool


class userUpdate(BaseModel):
    full_name: str | None
    is_active: bool | None
