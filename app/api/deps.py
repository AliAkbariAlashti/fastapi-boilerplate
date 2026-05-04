import uuid
from typing import Annotated

from app.db.repositories.snapshot_repo import SnapshotRepository
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.item_repo import ItemRepository
from app.models.user import User
from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.services.snapshot_service import SnapshotService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

DBSession = Annotated[AsyncSession, Depends(get_db)]


def get_user_repo(db: DBSession) -> UserRepository:
    return UserRepository(db)


def get_item_repo(db: DBSession) -> ItemRepository:
    return ItemRepository(db)

def get_snapshot_repo(db: DBSession) -> SnapshotRepository:
    return SnapshotRepository(db)

def get_user_service(repo: Annotated[UserRepository, Depends(get_user_repo)]) -> UserService:
    return UserService(repo)


def get_item_service(repo: Annotated[ItemRepository, Depends(get_item_repo)]) -> ItemService:
    return ItemService(repo)


def get_snapshot_service(repo: Annotated[SnapshotRepository, Depends(get_snapshot_repo)]) -> SnapshotService:
    return SnapshotService(repo)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, KeyError):
        raise credentials_exc

    user = await repo.get(user_id)
    if user is None or not user.is_active:
        raise credentials_exc
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
