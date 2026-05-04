import uuid
import math

from app.db.repositories.snapshot_repo import SnapshotRepository
from app.models.snapshot import Snapshot
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.snapshot import SnapshotRead, SnapshotCreate, SnapshotUpdate


class SnapshotService:
    def __init__(self, repo: SnapshotRepository) -> None:
        self.repo = repo

    async def list_for_owner(
        self, owner_id: uuid.UUID, pagination: PaginationParams
    ) -> PaginatedResponse[SnapshotRead]:
        snapshots, total = await self.repo.list_by_owner(
            owner_id, offset=pagination.offset, limit=pagination.size
        )
        return PaginatedResponse(
            snapshots=[SnapshotRead.model_validate(i) for i in snapshots],
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=math.ceil(total / pagination.size) if total else 0,
        )

    async def create(self, owner_id: uuid.UUID, data: SnapshotCreate) -> Snapshot:
        return await self.repo.create(
            snapshot_id=data.snapshot_id, data=data.data, owner_id=owner_id
        )

    async def get_owned(self, snapshot_id: uuid.UUID, owner_id: uuid.UUID) -> Snapshot:
        snapshot = await self.repo.get_or_raise(snapshot_id)
        if snapshot.owner_id != owner_id:
            raise PermissionError("Not authorized")
        return snapshot

    async def update(self, snapshot: Snapshot, data: SnapshotUpdate) -> Snapshot:
        updates = data.model_dump(exclude_none=True)
        return await self.repo.update(snapshot, **updates)

    async def delete(self, snapshot: Snapshot) -> None:
        await self.repo.delete(snapshot)
