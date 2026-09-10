# File: backend/app/application/use_cases/sync_patch_data.py

from typing import Any
from app.application.ports.riot_gateway import IRiotDataDragonGateway
from app.domain.repositories.patch_repository import IPatchRepository
from app.domain.repositories.champion_repository import IChampionRepository
from app.domain.repositories.item_repository import IItemRepository
from app.domain.repositories.rune_repository import IRuneRepository
from app.domain.repositories.spell_repository import ISpellRepository


class SyncPatchDataUseCase:
    """Use Case: Synchronizes current patch data from Data Dragon into the database."""

    def __init__(
        self,
        gateway: IRiotDataDragonGateway,
        patch_repo: IPatchRepository,
        champion_repo: IChampionRepository,
        item_repo: IItemRepository,
        rune_repo: IRuneRepository,
        spell_repo: ISpellRepository,
    ) -> None:
        self._gateway = gateway
        self._patch_repo = patch_repo
        self._champion_repo = champion_repo
        self._item_repo = item_repo
        self._rune_repo = rune_repo
        self._spell_repo = spell_repo

    async def execute(self, force: bool = False, locales: list[str] | None = None) -> dict[str, Any]:
        latest_version = await self._gateway.get_latest_version()
        active_version = await self._patch_repo.get_active_patch()

        if not force and active_version == latest_version:
            return {
                "status": "up_to_date",
                "patch": active_version,
                "message": f"Active patch {active_version} is already synchronized.",
            }

        target_locales = locales if locales is not None else ["vi_VN"]
        total_champs = 0
        total_items = 0
        total_runes = 0
        total_spells = 0

        for loc in target_locales:
            champions = await self._gateway.fetch_champions(latest_version, locale=loc)
            items = await self._gateway.fetch_items(latest_version, locale=loc)
            runes = await self._gateway.fetch_runes(latest_version, locale=loc)
            spells = await self._gateway.fetch_spells(latest_version, locale=loc)

            await self._champion_repo.upsert_many(champions, locale=loc)
            await self._item_repo.delete_all(locale=loc)
            await self._item_repo.upsert_many(items, locale=loc)
            await self._rune_repo.upsert_many(runes, locale=loc)
            await self._spell_repo.upsert_many(spells, locale=loc)

            total_champs += len(champions)
            total_items += len(items)
            total_runes += len(runes)
            total_spells += len(spells)

        await self._patch_repo.set_active_patch(latest_version)

        return {
            "status": "synchronized",
            "patch": latest_version,
            "locales": target_locales,
            "champions_count": total_champs,
            "items_count": total_items,
            "runes_count": total_runes,
            "spells_count": total_spells,
        }
