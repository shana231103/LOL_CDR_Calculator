# File: backend/tests/integration/test_sql_repositories.py

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.domain.enums import SkillSlot, HasteType
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell
from app.infrastructure.database.models.base import Base
from app.infrastructure.repositories.sql_champion_repo import SqlChampionRepository
from app.infrastructure.repositories.sql_item_repo import SqlItemRepository
from app.infrastructure.repositories.sql_rune_repo import SqlRuneRepository
from app.infrastructure.repositories.sql_spell_repo import SqlSpellRepository
from app.infrastructure.repositories.sql_patch_repo import SqlPatchRepository


@pytest.fixture
async def test_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.mark.anyio
async def test_champion_and_item_repo(test_session: AsyncSession):
    c_repo = SqlChampionRepository(test_session)
    i_repo = SqlItemRepository(test_session)

    champ = Champion(id="Lux", key="99", name="Lux", title="The Lady", image_url="http://lux.png")
    champ.add_ability(
        Ability(
            id="LuxQ",
            slot=SkillSlot.Q,
            name="Light Binding",
            description="Binds",
            image_url="",
            max_rank=5,
            cooldowns=[11.0, 10.5, 10.0, 9.5, 9.0],
        )
    )
    await c_repo.upsert_many([champ])

    item = Item(id=3001, name="Ludens", description="", image_url="", ability_haste=20.0, gold_total=3000)
    await i_repo.upsert_many([item])

    # Fetch back
    fetched_champ = await c_repo.get_by_id("Lux")
    assert fetched_champ is not None
    assert fetched_champ.name == "Lux"
    assert SkillSlot.Q in fetched_champ.abilities
    assert fetched_champ.abilities[SkillSlot.Q].max_rank == 5

    items = await i_repo.get_all("lud")
    assert len(items) == 1
    assert items[0].id == 3001
    assert items[0].ability_haste == 20.0

    await i_repo.delete_all()
    items_after_delete = await i_repo.get_all()
    assert len(items_after_delete) == 0



@pytest.mark.anyio
async def test_rune_spell_and_patch_repo(test_session: AsyncSession):
    r_repo = SqlRuneRepository(test_session)
    s_repo = SqlSpellRepository(test_session)
    p_repo = SqlPatchRepository(test_session)

    rune = Rune(
        id=8106,
        key="UltimateHunter",
        name="Ultimate Hunter",
        icon_url="",
        haste_type=HasteType.ULTIMATE_HASTE,
        base_haste=6.0,
        haste_per_stack=5.0,
        max_stacks=5,
    )
    await r_repo.upsert_many([rune])

    spell = SummonerSpell(id="Flash", key="4", name="Flash", description="", cooldown=300.0, image_url="")
    await s_repo.upsert_many([spell])

    await p_repo.set_active_patch("15.4.1")

    runes = await r_repo.get_haste_runes()
    assert len(runes) == 1
    assert runes[0].haste_type == HasteType.ULTIMATE_HASTE

    spells = await s_repo.get_by_ids(["Flash"])
    assert len(spells) == 1
    assert spells[0].cooldown == 300.0

    active_p = await p_repo.get_active_patch()
    assert active_p == "15.4.1"
