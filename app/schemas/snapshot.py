import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

class SnapshotBase(BaseModel):
    snapshot_id: uuid.UUID
    data: dict[str, Any]

class SnapshotCreate(SnapshotBase):
    pass

class SnapshotUpdate(BaseModel):
    snapshot_id: uuid.UUID | None = None
    data: dict[str, Any] | None = None

class SnapshotRead(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    snapshot_id: uuid.UUID
    data: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}
