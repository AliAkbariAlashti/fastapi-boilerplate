import uuid
import math

from app.db.repositories.item_repo import ItemRepository
from app.models.item import Item
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate


class ItemService:
    def __init__(self, repo: ItemRepository) -> None:
        self.repo = repo

    async def list_for_owner(
        self, owner_id: uuid.UUID, pagination: PaginationParams
    ) -> PaginatedResponse[ItemRead]:
        items, total = await self.repo.list_by_owner(
            owner_id, offset=pagination.offset, limit=pagination.size
        )
        return PaginatedResponse(
            items=[ItemRead.model_validate(i) for i in items],
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=math.ceil(total / pagination.size) if total else 0,
        )

    async def create(self, owner_id: uuid.UUID, data: ItemCreate) -> Item:
        return await self.repo.create(
            title=data.title, description=data.description, owner_id=owner_id
        )

    async def get_owned(self, item_id: uuid.UUID, owner_id: uuid.UUID) -> Item:
        item = await self.repo.get_or_raise(item_id)
        if item.owner_id != owner_id:
            raise PermissionError("Not authorized")
        return item

    async def update(self, item: Item, data: ItemUpdate) -> Item:
        updates = data.model_dump(exclude_none=True)
        return await self.repo.update(item, **updates)

    async def delete(self, item: Item) -> None:
        await self.repo.delete(item)
