# File: backend/tests/integration/test_api_calculate.py

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.domain.enums import SkillSlot, HasteType
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell
from app.infrastructure.database.models.base import Base
from app.infrastructure.database.session import get_async_session
from app.infrastructure.repositories.sql_champion_repo import SqlChampionRepository
from app.infrastructure.repositories.sql_item_repo import SqlItemRepository
from app.infrastructure.repositories.sql_rune_repo import SqlRuneRepository
from app.infrastructure.repositories.sql_spell_repo import SqlSpellRepository
from app.main import app


@pytest.fixture
async def setup_test_app():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_async_session():
        async with session_maker() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_async_session] = override_get_async_session

    # Seed test data
    async with session_maker() as session:
        c_repo = SqlChampionRepository(session)
        i_repo = SqlItemRepository(session)
        r_repo = SqlRuneRepository(session)
        s_repo = SqlSpellRepository(session)

        champ = Champion(id="Ahri", key="103", name="Ahri", title="Fox", image_url="")
        champ.add_ability(
            Ability(
                id="AhriQ",
                slot=SkillSlot.Q,
                name="Orb",
                description="",
                image_url="",
                max_rank=5,
                cooldowns=[7.0, 7.0, 7.0, 7.0, 7.0],
            )
        )
        champ.add_ability(
            Ability(
                id="AhriR",
                slot=SkillSlot.R,
                name="Spirit Rush",
                description="",
                image_url="",
                max_rank=3,
                cooldowns=[130.0, 105.0, 80.0],
            )
        )
        await c_repo.upsert_many([champ])

        item = Item(id=3001, name="ItemAH", description="", image_url="", ability_haste=20.0)
        await i_repo.upsert_many([item])

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
        await session.commit()

    yield

    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.anyio
async def test_api_calculate_endpoint(setup_test_app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "champion_id": "Ahri",
            "abilities": {"Q": 5, "R": 1},
            "items": [3001],
            "runes": [{"rune_id": 8106, "stacks": 2}],
            "summoner_spells": ["Flash"],
        }
        resp = await client.post("/api/v1/calculate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["champion_id"] == "Ahri"
        assert data["ability_haste"] == 20.0
        assert data["ultimate_haste"] == 16.0  # 6 + 2*5 = 16
        # Q: 7.0 * 100 / 120 = 5.83
        assert data["abilities"]["Q"]["final_cooldown"] == 5.83
        # R: 130 * 100 / (100 + 20 + 16) = 130 * 100 / 136 = 95.59
        assert data["abilities"]["R"]["final_cooldown"] == 95.59


@pytest.mark.anyio
async def test_api_calculate_champion_not_found(setup_test_app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/calculate", json={"champion_id": "NonExistent"})
        assert resp.status_code == 404
        assert resp.json()["error"] == "NOT_FOUND"


@pytest.mark.anyio
async def test_api_calculate_invalid_rank(setup_test_app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "champion_id": "Ahri",
            "abilities": {"Q": 10},  # max rank is 5
        }
        resp = await client.post("/api/v1/calculate", json=payload)
        assert resp.status_code == 400
        assert resp.json()["error"] == "INVALID_RANK"
