import sys
sys.path.insert(0, ".")
import asyncio
from app.infrastructure.database.session import get_session_factory
from app.infrastructure.repositories.sql_champion_repo import SqlChampionRepository
from app.infrastructure.repositories.sql_item_repo import SqlItemRepository
from app.infrastructure.repositories.sql_rune_repo import SqlRuneRepository
from app.infrastructure.repositories.sql_spell_repo import SqlSpellRepository
from app.infrastructure.repositories.sql_patch_repo import SqlPatchRepository
from app.infrastructure.external.riot_client import RiotDataDragonClient
from app.application.use_cases.sync_patch_data import SyncPatchDataUseCase

async def main():
    factory = get_session_factory()
    async with factory() as session:
        uc = SyncPatchDataUseCase(
            gateway=RiotDataDragonClient(),
            patch_repo=SqlPatchRepository(session),
            champion_repo=SqlChampionRepository(session),
            item_repo=SqlItemRepository(session),
            rune_repo=SqlRuneRepository(session),
            spell_repo=SqlSpellRepository(session),
        )
        print("Starting sync...")
        res = await uc.execute(force=True)
        print("Sync completed successfully:", res)
        await session.commit()

asyncio.run(main())
