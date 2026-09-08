# File: backend/app/domain/repositories/item_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.item import Item


class IItemRepository(ABC):
    """Port interface for Item persistence."""

    @abstractmethod
    async def get_all(self, search: str | None = None) -> list[Item]:
        """Returns all items matching an optional search term."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, item_ids: list[int]) -> list[Item]:
        """Returns items matching the given list of IDs."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, items: list[Item]) -> None:
        """Inserts or updates a collection of items."""
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self) -> None:
        """Deletes all item records from persistence storage."""
        raise NotImplementedError

