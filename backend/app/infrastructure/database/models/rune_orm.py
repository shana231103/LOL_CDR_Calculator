# File: backend/app/infrastructure/database/models/rune_orm.py

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base


class RuneORM(Base):
    __tablename__ = "runes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    locale: Mapped[str] = mapped_column(String(10), primary_key=True, default="vi_VN")
    key: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(100))
    icon_url: Mapped[str] = mapped_column(String(255), default="")
    haste_type: Mapped[str] = mapped_column(String(30))
    base_haste: Mapped[float] = mapped_column(Float, default=0.0)
    haste_per_stack: Mapped[float] = mapped_column(Float, default=0.0)
    max_stacks: Mapped[int] = mapped_column(Integer, default=0)
