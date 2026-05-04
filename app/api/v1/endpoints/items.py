import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import CurrentUser, get_item_service
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=PaginatedResponse[ItemRead])
async def list_items(
    current_user: CurrentUser,
    svc: Annotated[ItemService, Depends(get_item_service)],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[ItemRead]:
    return await svc.list_for_owner(current_user.id, PaginationParams(page=page, size=size))


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    current_user: CurrentUser,
    svc: Annotated[ItemService, Depends(get_item_service)],
) -> ItemRead:
    item = await svc.create(current_user.id, data)
    return ItemRead.model_validate(item)


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: uuid.UUID,
    current_user: CurrentUser,
    svc: Annotated[ItemService, Depends(get_item_service)],
) -> ItemRead:
    try:
        item = await svc.get_owned(item_id, current_user.id)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return ItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: uuid.UUID,
    data: ItemUpdate,
    current_user: CurrentUser,
    svc: Annotated[ItemService, Depends(get_item_service)],
) -> ItemRead:
    try:
        item = await svc.get_owned(item_id, current_user.id)
        item = await svc.update(item, data)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return ItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: uuid.UUID,
    current_user: CurrentUser,
    svc: Annotated[ItemService, Depends(get_item_service)],
) -> None:
    try:
        item = await svc.get_owned(item_id, current_user.id)
        await svc.delete(item)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
