import uuid

from app.db.repositories.base import BaseRepository
from app.models.item import Item


class ItemRepository(BaseRepository[Item]):
    model = Item

    async def list_by_owner(
        self, owner_id: uuid.UUID, *, offset: int = 0, limit: int = 20
    ) -> tuple[list[Item], int]:
        return await self.list(offset=offset, limit=limit, owner_id=owner_id)
