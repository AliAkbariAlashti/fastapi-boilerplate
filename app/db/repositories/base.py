import uuid
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: uuid.UUID) -> ModelT | None:
        return await self.session.get(self.model, id)

    async def get_or_raise(self, id: uuid.UUID) -> ModelT:
        obj = await self.get(id)
        if obj is None:
            raise ValueError(f"{self.model.__name__} {id} not found")
        return obj

    async def list(
        self, *, offset: int = 0, limit: int = 20, **filters: Any
    ) -> tuple[list[ModelT], int]:
        query = select(self.model)
        for key, value in filters.items():
            query = query.where(getattr(self.model, key) == value)

        count_result = await self.session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar_one()

        result = await self.session.execute(query.offset(offset).limit(limit))
        return list(result.scalars().all()), total

    async def create(self, **kwargs: Any) -> ModelT:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelT, **kwargs: Any) -> ModelT:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self.session.delete(obj)
        await self.session.flush()
