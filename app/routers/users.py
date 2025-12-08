from fastapi import APIRouter, Depends, Query
from typing import Sequence

from app.dependencies.user_dependencies import get_user_service
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserRead,
    responses={
        409: {"description": "Email already registered"},
        422: {"description": "Invalid input"},
    },
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.register_user(payload)
    return user


@router.get("/", response_model=Sequence[UserRead])
def list_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: UserService = Depends(get_user_service),
):
    return svc.list_users(limit=limit, offset=offset)
