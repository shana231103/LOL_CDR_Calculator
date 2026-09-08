# File: backend/app/infrastructure/database/models/item_orm.py

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base


class ItemORM(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String(1000), default="")
    image_url: Mapped[str] = mapped_column(String(255), default="")
    ability_haste: Mapped[float] = mapped_column(Float, default=0.0)
    ultimate_haste: Mapped[float] = mapped_column(Float, default=0.0)
    basic_haste: Mapped[float] = mapped_column(Float, default=0.0)
    summoner_haste: Mapped[float] = mapped_column(Float, default=0.0)
    gold_total: Mapped[int] = mapped_column(Integer, default=0)
