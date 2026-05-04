import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Item(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "items"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    owner: Mapped["User"] = relationship("User", lazy="selectin")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Item id={self.id} title={self.title}>"
