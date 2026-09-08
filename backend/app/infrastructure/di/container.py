# File: backend/app/infrastructure/di/container.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_async_session
from app.infrastructure.config.settings import get_settings, Settings
from app.domain.repositories.champion_repository import IChampionRepository
from app.domain.repositories.item_repository import IItemRepository
from app.domain.repositories.rune_repository import IRuneRepository
from app.domain.repositories.spell_repository import ISpellRepository
from app.domain.repositories.patch_repository import IPatchRepository
from app.application.ports.riot_gateway import IRiotDataDragonGateway
from app.infrastructure.repositories.sql_champion_repo import SqlChampionRepository
from app.infrastructure.repositories.sql_item_repo import SqlItemRepository
from app.infrastructure.repositories.sql_rune_repo import SqlRuneRepository
from app.infrastructure.repositories.sql_spell_repo import SqlSpellRepository
from app.infrastructure.repositories.sql_patch_repo import SqlPatchRepository
from app.infrastructure.external.riot_client import RiotDataDragonClient
from app.application.use_cases.calculate_cooldown import CalculateCooldownUseCase
from app.application.use_cases.sync_patch_data import SyncPatchDataUseCase
from app.application.use_cases.get_champions import (
    GetChampionsUseCase,
    GetChampionByIdUseCase,
)
from app.application.use_cases.get_items import GetItemsUseCase
from app.application.use_cases.get_runes import GetRunesUseCase
from app.application.use_cases.get_spells import GetSpellsUseCase


def get_champion_repo(
    session: AsyncSession = Depends(get_async_session),
) -> IChampionRepository:
    return SqlChampionRepository(session)


def get_item_repo(
    session: AsyncSession = Depends(get_async_session),
) -> IItemRepository:
    return SqlItemRepository(session)


def get_rune_repo(
    session: AsyncSession = Depends(get_async_session),
) -> IRuneRepository:
    return SqlRuneRepository(session)


def get_spell_repo(
    session: AsyncSession = Depends(get_async_session),
) -> ISpellRepository:
    return SqlSpellRepository(session)


def get_patch_repo(
    session: AsyncSession = Depends(get_async_session),
) -> IPatchRepository:
    return SqlPatchRepository(session)


def get_riot_gateway(
    settings: Settings = Depends(get_settings),
) -> IRiotDataDragonGateway:
    return RiotDataDragonClient(cdn_base=settings.riot_ddragon_cdn)


def get_calculate_cooldown_use_case(
    c_repo: IChampionRepository = Depends(get_champion_repo),
    i_repo: IItemRepository = Depends(get_item_repo),
    r_repo: IRuneRepository = Depends(get_rune_repo),
    s_repo: ISpellRepository = Depends(get_spell_repo),
) -> CalculateCooldownUseCase:
    return CalculateCooldownUseCase(c_repo, i_repo, r_repo, s_repo)


def get_sync_patch_use_case(
    gateway: IRiotDataDragonGateway = Depends(get_riot_gateway),
    p_repo: IPatchRepository = Depends(get_patch_repo),
    c_repo: IChampionRepository = Depends(get_champion_repo),
    i_repo: IItemRepository = Depends(get_item_repo),
    r_repo: IRuneRepository = Depends(get_rune_repo),
    s_repo: ISpellRepository = Depends(get_spell_repo),
) -> SyncPatchDataUseCase:
    return SyncPatchDataUseCase(gateway, p_repo, c_repo, i_repo, r_repo, s_repo)


def get_champions_use_case(
    c_repo: IChampionRepository = Depends(get_champion_repo),
) -> GetChampionsUseCase:
    return GetChampionsUseCase(c_repo)


def get_champion_by_id_use_case(
    c_repo: IChampionRepository = Depends(get_champion_repo),
) -> GetChampionByIdUseCase:
    return GetChampionByIdUseCase(c_repo)


def get_items_use_case(
    i_repo: IItemRepository = Depends(get_item_repo),
) -> GetItemsUseCase:
    return GetItemsUseCase(i_repo)


def get_runes_use_case(
    r_repo: IRuneRepository = Depends(get_rune_repo),
) -> GetRunesUseCase:
    return GetRunesUseCase(r_repo)


def get_spells_use_case(
    s_repo: ISpellRepository = Depends(get_spell_repo),
) -> GetSpellsUseCase:
    return GetSpellsUseCase(s_repo)
