# File: backend/app/domain/repositories/__init__.py

from app.domain.repositories.champion_repository import IChampionRepository
from app.domain.repositories.item_repository import IItemRepository
from app.domain.repositories.rune_repository import IRuneRepository
from app.domain.repositories.spell_repository import ISpellRepository
from app.domain.repositories.patch_repository import IPatchRepository

__all__ = [
    "IChampionRepository",
    "IItemRepository",
    "IRuneRepository",
    "ISpellRepository",
    "IPatchRepository",
]
