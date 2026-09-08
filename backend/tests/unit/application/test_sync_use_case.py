# File: backend/tests/unit/application/test_sync_use_case.py

import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.sync_patch_data import SyncPatchDataUseCase
from app.domain.entities.item import Item
from app.domain.entities.champion import Champion
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell
from app.domain.enums import HasteType


@pytest.mark.anyio
async def test_sync_patch_data_prunes_items_before_upsert():
    gateway = AsyncMock()
    patch_repo = AsyncMock()
    champion_repo = AsyncMock()
    item_repo = AsyncMock()
    rune_repo = AsyncMock()
    spell_repo = AsyncMock()

    gateway.get_latest_version.return_value = "15.4.1"
    patch_repo.get_active_patch.return_value = "15.3.1"

    test_item = Item(id=3071, name="Black Cleaver", description="", image_url="", ability_haste=20.0, gold_total=3000)
    gateway.fetch_champions.return_value = []
    gateway.fetch_items.return_value = [test_item]
    gateway.fetch_runes.return_value = []
    gateway.fetch_spells.return_value = []

    call_order = []
    item_repo.delete_all.side_effect = lambda: call_order.append("delete_all")
    item_repo.upsert_many.side_effect = lambda items: call_order.append("upsert_many")

    use_case = SyncPatchDataUseCase(
        gateway=gateway,
        patch_repo=patch_repo,
        champion_repo=champion_repo,
        item_repo=item_repo,
        rune_repo=rune_repo,
        spell_repo=spell_repo,
    )

    result = await use_case.execute(force=False)

    assert result["status"] == "synchronized"
    assert result["patch"] == "15.4.1"
    assert result["items_count"] == 1

    # Verify delete_all was called strictly before upsert_many
    item_repo.delete_all.assert_awaited_once()
    item_repo.upsert_many.assert_awaited_once_with([test_item])
    assert call_order == ["delete_all", "upsert_many"]
