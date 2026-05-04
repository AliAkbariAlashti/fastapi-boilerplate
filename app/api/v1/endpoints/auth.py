from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_user_service
from app.schemas.user import Token, UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    svc: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    try:
        user = await svc.register(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return UserRead.model_validate(user)


@router.post("/token", response_model=Token)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    svc: Annotated[UserService, Depends(get_user_service)],
) -> Token:
    try:
        return await svc.authenticate(form.username, form.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
