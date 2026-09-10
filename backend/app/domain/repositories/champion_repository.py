# File: backend/app/domain/repositories/champion_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.champion import Champion


class IChampionRepository(ABC):
    """Port interface for Champion persistence."""

    @abstractmethod
    async def get_all(self, locale: str = "vi_VN") -> list[Champion]:
        """Returns all champions available in the database for the given locale."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, champion_id: str, locale: str | None = None) -> Champion | None:
        """Returns a single champion by ID or None if not found, optionally filtered by locale."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, champions: list[Champion], locale: str = "vi_VN") -> None:
        """Inserts or updates a collection of champions with their abilities for the given locale."""
        raise NotImplementedError
