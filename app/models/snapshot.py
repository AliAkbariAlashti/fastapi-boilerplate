import uuid
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Snapshot(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "snapshots"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    owner: Mapped["User"] = relationship("User", lazy="selectin")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Snapshot id={self.id} owner_id={self.owner_id} snapshot_id={self.snapshot_id}>"
