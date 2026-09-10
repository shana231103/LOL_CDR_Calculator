# File: backend/app/domain/repositories/item_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.item import Item


class IItemRepository(ABC):
    """Port interface for Item persistence."""

    @abstractmethod
    async def get_all(self, search: str | None = None, locale: str = "vi_VN") -> list[Item]:
        """Returns all items matching an optional search term and locale."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, item_ids: list[int], locale: str | None = None) -> list[Item]:
        """Returns items matching the given list of IDs, optionally filtered by locale."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, items: list[Item], locale: str = "vi_VN") -> None:
        """Inserts or updates a collection of items for the given locale."""
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, locale: str | None = None) -> None:
        """Deletes item records from persistence storage, optionally filtered by locale."""
        raise NotImplementedError

