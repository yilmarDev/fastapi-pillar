from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Sequence

from app.db.database import get_session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)


@router.post("/", response_model=UserRead)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.register_user(payload)
    return user


@router.get("/", response_model=Sequence[UserRead])
def list_users(
    limit: int = 100, offset: int = 0, svc: UserService = Depends(get_user_service)
):
    return svc.list_users(limit=limit, offtset=offset)
