# File: backend/app/infrastructure/di/__init__.py

from app.infrastructure.di.container import (
    get_champion_repo,
    get_item_repo,
    get_rune_repo,
    get_spell_repo,
    get_patch_repo,
    get_riot_gateway,
    get_calculate_cooldown_use_case,
    get_sync_patch_use_case,
    get_champions_use_case,
    get_champion_by_id_use_case,
    get_items_use_case,
    get_runes_use_case,
    get_spells_use_case,
)

__all__ = [
    "get_champion_repo",
    "get_item_repo",
    "get_rune_repo",
    "get_spell_repo",
    "get_patch_repo",
    "get_riot_gateway",
    "get_calculate_cooldown_use_case",
    "get_sync_patch_use_case",
    "get_champions_use_case",
    "get_champion_by_id_use_case",
    "get_items_use_case",
    "get_runes_use_case",
    "get_spells_use_case",
]
