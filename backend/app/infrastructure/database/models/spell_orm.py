# File: backend/app/infrastructure/database/models/spell_orm.py

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base


class SpellORM(Base):
    __tablename__ = "summoner_spells"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    key: Mapped[str] = mapped_column(String(20), index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000), default="")
    cooldown: Mapped[float] = mapped_column(Float, default=0.0)
    image_url: Mapped[str] = mapped_column(String(255), default="")
