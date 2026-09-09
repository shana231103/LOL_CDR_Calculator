# File: backend/tests/integration/test_api_items.py

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.domain.entities.item import Item
from app.infrastructure.database.models.base import Base
from app.infrastructure.database.session import get_async_session
from app.infrastructure.repositories.sql_item_repo import SqlItemRepository
from app.main import app


@pytest.fixture
async def setup_items_test_app():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_async_session():
        async with session_maker() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with session_maker() as session:
        i_repo = SqlItemRepository(session)
        items = [
            Item(
                id=3118,
                name="Malignance",
                description="Gain 20 Ultimate Ability Haste.",
                image_url="http://example.com/3118.png",
                ability_haste=15.0,
                ultimate_haste=20.0,
                basic_haste=0.0,
                summoner_haste=0.0,
                gold_total=3000,
            ),
            Item(
                id=3161,
                name="Spear of Shojin",
                description="Gain 25 Basic Ability Haste.",
                image_url="http://example.com/3161.png",
                ability_haste=0.0,
                ultimate_haste=0.0,
                basic_haste=25.0,
                summoner_haste=0.0,
                gold_total=3100,
            ),
            Item(
                id=3158,
                name="Ionian Boots of Lucidity",
                description="Gain 10 Summoner Spell Haste.",
                image_url="http://example.com/3158.png",
                ability_haste=10.0,
                ultimate_haste=0.0,
                basic_haste=0.0,
                summoner_haste=10.0,
                gold_total=900,
            ),
        ]
        await i_repo.upsert_many(items)
        await session.commit()

    yield

    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.anyio
async def test_list_items_returns_specialized_haste(setup_items_test_app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        item_map = {item["id"]: item for item in data}

        malignance = item_map[3118]
        assert malignance["name"] == "Malignance"
        assert malignance["ability_haste"] == 15.0
        assert malignance["ultimate_haste"] == 20.0
        assert malignance["basic_haste"] == 0.0
        assert malignance["summoner_haste"] == 0.0

        shojin = item_map[3161]
        assert shojin["name"] == "Spear of Shojin"
        assert shojin["ability_haste"] == 0.0
        assert shojin["ultimate_haste"] == 0.0
        assert shojin["basic_haste"] == 25.0
        assert shojin["summoner_haste"] == 0.0

        boots = item_map[3158]
        assert boots["name"] == "Ionian Boots of Lucidity"
        assert boots["ability_haste"] == 10.0
        assert boots["ultimate_haste"] == 0.0
        assert boots["basic_haste"] == 0.0
        assert boots["summoner_haste"] == 10.0


@pytest.mark.anyio
async def test_list_items_search_filter(setup_items_test_app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/items?search=Malignance")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 3118
        assert data[0]["ultimate_haste"] == 20.0
