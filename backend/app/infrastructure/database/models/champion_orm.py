# File: backend/app/infrastructure/database/models/champion_orm.py

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.ability_orm import AbilityORM


class ChampionORM(Base):
    __tablename__ = "champions"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    locale: Mapped[str] = mapped_column(String(10), primary_key=True, default="vi_VN")
    key: Mapped[str] = mapped_column(String(20), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(String(150))
    image_url: Mapped[str] = mapped_column(String(255))

    abilities: Mapped[list["AbilityORM"]] = relationship(
        "AbilityORM",
        back_populates="champion",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
