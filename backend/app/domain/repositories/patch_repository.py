# File: backend/app/domain/repositories/patch_repository.py

from abc import ABC, abstractmethod


class IPatchRepository(ABC):
    """Port interface for active game patch persistence."""

    @abstractmethod
    async def get_active_patch(self) -> str | None:
        """Retrieves the active patch version string from storage."""
        raise NotImplementedError

    @abstractmethod
    async def set_active_patch(self, patch_version: str) -> None:
        """Sets or updates the active patch version in storage."""
        raise NotImplementedError
