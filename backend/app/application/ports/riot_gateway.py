# File: backend/app/application/ports/riot_gateway.py

from abc import ABC, abstractmethod
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell


class IRiotDataDragonGateway(ABC):
    """Port interface for Riot Data Dragon external gateway."""

    @abstractmethod
    async def get_latest_version(self) -> str:
        """Fetches the latest active patch version string from Data Dragon CDN."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_champions(self, version: str) -> list[Champion]:
        """Fetches full champion data with abilities for the given patch version."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_items(self, version: str) -> list[Item]:
        """Fetches item data with ability haste values for the given patch version."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_runes(self, version: str) -> list[Rune]:
        """Fetches haste-related runes with metadata for the given patch version."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_spells(self, version: str) -> list[SummonerSpell]:
        """Fetches summoner spells for the given patch version."""
        raise NotImplementedError
