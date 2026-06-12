from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Response schema for login endpoint"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data extracted from JWT token payload"""

    email: str | None = None


class UserLogin(BaseModel):
    """Request schema for user login"""

    email: EmailStr
    password: str
