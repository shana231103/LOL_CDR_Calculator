# File: backend/app/infrastructure/database/models/patch_orm.py

from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base


class PatchORM(Base):
    __tablename__ = "active_patch"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    version: Mapped[str] = mapped_column(String(30))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
