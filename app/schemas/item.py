import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class ItemRead(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
