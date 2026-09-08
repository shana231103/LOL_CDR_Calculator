# File: backend/app/infrastructure/database/models/ability_orm.py

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.champion_orm import ChampionORM


class AbilityORM(Base):
    __tablename__ = "abilities"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    champion_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("champions.id", ondelete="CASCADE"),
        index=True,
    )
    slot: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000), default="")
    image_url: Mapped[str] = mapped_column(String(255), default="")
    max_rank: Mapped[int] = mapped_column(Integer, default=5)
    cooldowns: Mapped[list[float]] = mapped_column(JSON, default=list)

    champion: Mapped["ChampionORM"] = relationship(
        "ChampionORM",
        back_populates="abilities",
    )
