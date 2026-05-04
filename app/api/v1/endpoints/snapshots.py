import uuid
from typing import Annotated

from app.db.repositories.snapshot_repo import SnapshotRepository
from app.schemas.snapshot import SnapshotCreate, SnapshotRead, SnapshotUpdate
from app.services.snapshot_service import SnapshotService
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import CurrentUser, get_item_service, get_snapshot_service
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item_service import ItemService


router = APIRouter(prefix="/snapshots", tags=["snapshots"])

@router.get("/", response_model=PaginatedResponse[SnapshotRead])
async def list_Snapshots(
    current_user: CurrentUser,
    svc: Annotated[SnapshotService, Depends(get_snapshot_service)],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[SnapshotRead]:
    return await svc.list_for_owner(current_user.id, PaginationParams(page=page, size=size))


@router.post("/", response_model=SnapshotRead, status_code=status.HTTP_201_CREATED)
async def create_snapshot(
    data: SnapshotCreate,
    current_user: CurrentUser,
    svc: Annotated[SnapshotService, Depends(get_snapshot_service)],
) -> SnapshotRead:
    snapshot = await svc.create(current_user.id, data)
    return SnapshotRead.model_validate(snapshot)

@router.get("/{snapshot_id}", response_model=SnapshotRead)
async def get_snapshot(
    snapshot_id: uuid.UUID,
    current_user: CurrentUser,
    svc: Annotated[SnapshotService, Depends(get_snapshot_service)],
) -> SnapshotRead:
    try:
        snapshot = await svc.get_owned(snapshot_id, current_user.id)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return SnapshotRead.model_validate(snapshot)


@router.patch("/{snapshot_id}", response_model=SnapshotRead)
async def update_snapshot(
    snapshot_id: uuid.UUID,
    data: SnapshotUpdate,
    current_user: CurrentUser,
    svc: Annotated[SnapshotService, Depends(get_snapshot_service)],
) -> SnapshotRead:
    try:
        snapshot = await svc.get_owned(snapshot_id, current_user.id)
        snapshot = await svc.update(snapshot, data)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return SnapshotRead.model_validate(snapshot)


@router.delete("/{snapshot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_snapshot(
    snapshot_id: uuid.UUID,
    current_user: CurrentUser,
    svc: Annotated[SnapshotService, Depends(get_snapshot_service)],
) -> None:
    try:
        snapshot = await svc.get_owned(snapshot_id, current_user.id)
        await svc.delete(snapshot)
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))