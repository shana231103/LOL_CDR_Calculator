# File: backend/app/domain/repositories/champion_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.champion import Champion


class IChampionRepository(ABC):
    """Port interface for Champion persistence."""

    @abstractmethod
    async def get_all(self) -> list[Champion]:
        """Returns all champions available in the database."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, champion_id: str) -> Champion | None:
        """Returns a single champion by ID or None if not found."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, champions: list[Champion]) -> None:
        """Inserts or updates a collection of champions with their abilities."""
        raise NotImplementedError
