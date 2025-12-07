from fastapi import APIRouter, Depends, HTTPException, status
from typing import Sequence

from app.dependencies.user_dependencies import get_user_service
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


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
