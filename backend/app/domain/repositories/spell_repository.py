# File: backend/app/domain/repositories/spell_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.spell import SummonerSpell


class ISpellRepository(ABC):
    """Port interface for Summoner Spell persistence."""

    @abstractmethod
    async def get_all(self, locale: str = "vi_VN") -> list[SummonerSpell]:
        """Returns all summoner spells available for the given locale."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, spell_ids: list[str], locale: str | None = None) -> list[SummonerSpell]:
        """Returns summoner spells matching the given list of IDs, optionally filtered by locale."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, spells: list[SummonerSpell], locale: str = "vi_VN") -> None:
        """Inserts or updates a collection of summoner spells for the given locale."""
        raise NotImplementedError
