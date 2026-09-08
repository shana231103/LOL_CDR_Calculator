# File: backend/app/domain/repositories/spell_repository.py

from abc import ABC, abstractmethod
from app.domain.entities.spell import SummonerSpell


class ISpellRepository(ABC):
    """Port interface for Summoner Spell persistence."""

    @abstractmethod
    async def get_all(self) -> list[SummonerSpell]:
        """Returns all summoner spells available."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, spell_ids: list[str]) -> list[SummonerSpell]:
        """Returns summoner spells matching the given list of IDs."""
        raise NotImplementedError

    @abstractmethod
    async def upsert_many(self, spells: list[SummonerSpell]) -> None:
        """Inserts or updates a collection of summoner spells."""
        raise NotImplementedError
