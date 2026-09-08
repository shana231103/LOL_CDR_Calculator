# File: backend/app/domain/repositories/rune_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.rune import Rune


class IRuneRepository(ABC):
    """Port interface for Rune persistence."""

    @abstractmethod
    async def get_haste_runes(self) -> list[Rune]:
        """Returns all runes providing ability/ultimate/summoner haste."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, rune_ids: list[int]) -> list[Rune]:
        """Returns runes matching the given list of IDs."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, runes: list[Rune]) -> None:
        """Inserts or updates a collection of haste runes."""
        raise NotImplementedError
