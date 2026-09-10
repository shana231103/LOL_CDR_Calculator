# File: backend/tests/integration/test_api_locale.py

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell
from app.domain.enums import HasteType
from app.infrastructure.database.models.base import Base
from app.infrastructure.database.session import get_async_session
from app.infrastructure.repositories.sql_champion_repo import SqlChampionRepository
from app.infrastructure.repositories.sql_item_repo import SqlItemRepository
from app.infrastructure.repositories.sql_rune_repo import SqlRuneRepository
from app.infrastructure.repositories.sql_spell_repo import SqlSpellRepository
from app.main import app


@pytest.fixture
async def setup_locale_test_app():
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
        c_repo = SqlChampionRepository(session)
        i_repo = SqlItemRepository(session)
        r_repo = SqlRuneRepository(session)
        s_repo = SqlSpellRepository(session)

        # Seed vi_VN data
        champ_vi = Champion(id="Aatrox", key="266", name="Aatrox", title="Quỷ Kiếm Darkin", image_url="http://aatrox.png", locale="vi_VN")
        item_vi = Item(id=3067, name="Hỏa Ngọc", description="10 Điểm Hồi Kỹ Năng", image_url="http://3067.png", ability_haste=10.0, locale="vi_VN")
        rune_vi = Rune(id=8106, key="UltimateHunter", name="Thợ Săn Tối Thượng", icon_url="http://8106.png", haste_type=HasteType.ULTIMATE_HASTE, base_haste=6.0, locale="vi_VN")
        spell_vi = SummonerSpell(id="SummonerFlash", key="4", name="Tốc Biến", description="Dịch chuyển", cooldown=300.0, image_url="http://flash.png", locale="vi_VN")

        await c_repo.upsert_many([champ_vi], locale="vi_VN")
        await i_repo.upsert_many([item_vi], locale="vi_VN")
        await r_repo.upsert_many([rune_vi], locale="vi_VN")
        await s_repo.upsert_many([spell_vi], locale="vi_VN")

        # Seed en_US data
        champ_en = Champion(id="Aatrox", key="266", name="Aatrox", title="the Darkin Blade", image_url="http://aatrox.png", locale="en_US")
        item_en = Item(id=3067, name="Kindlegem", description="10 Ability Haste", image_url="http://3067.png", ability_haste=10.0, locale="en_US")
        rune_en = Rune(id=8106, key="UltimateHunter", name="Ultimate Hunter", icon_url="http://8106.png", haste_type=HasteType.ULTIMATE_HASTE, base_haste=6.0, locale="en_US")
        spell_en = SummonerSpell(id="SummonerFlash", key="4", name="Flash", description="Teleports", cooldown=300.0, image_url="http://flash.png", locale="en_US")

        await c_repo.upsert_many([champ_en], locale="en_US")
        await i_repo.upsert_many([item_en], locale="en_US")
        await r_repo.upsert_many([rune_en], locale="en_US")
        await s_repo.upsert_many([spell_en], locale="en_US")

        await session.commit()

    yield

    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.anyio
async def test_get_champions_by_locale(setup_locale_test_app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. vi_VN
        res_vi = await client.get("/api/v1/champions?locale=vi_VN")
        assert res_vi.status_code == 200
        data_vi = res_vi.json()
        assert len(data_vi) == 1
        assert data_vi[0]["title"] == "Quỷ Kiếm Darkin"

        # 2. en_US
        res_en = await client.get("/api/v1/champions?locale=en_US")
        assert res_en.status_code == 200
        data_en = res_en.json()
        assert len(data_en) == 1
        assert data_en[0]["title"] == "the Darkin Blade"

        # 3. Invalid locale
        res_err = await client.get("/api/v1/champions?locale=fr_FR")
        assert res_err.status_code == 422


@pytest.mark.anyio
async def test_get_items_by_locale(setup_locale_test_app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_vi = await client.get("/api/v1/items?locale=vi_VN")
        assert res_vi.status_code == 200
        assert res_vi.json()[0]["name"] == "Hỏa Ngọc"

        res_en = await client.get("/api/v1/items?locale=en_US")
        assert res_en.status_code == 200
        assert res_en.json()[0]["name"] == "Kindlegem"


@pytest.mark.anyio
async def test_get_runes_and_spells_by_locale(setup_locale_test_app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Runes
        res_r_vi = await client.get("/api/v1/runes?locale=vi_VN")
        assert res_r_vi.status_code == 200
        assert res_r_vi.json()[0]["name"] == "Thợ Săn Tối Thượng"

        res_r_en = await client.get("/api/v1/runes?locale=en_US")
        assert res_r_en.status_code == 200
        assert res_r_en.json()[0]["name"] == "Ultimate Hunter"

        # Spells
        res_s_vi = await client.get("/api/v1/summoner-spells?locale=vi_VN")
        assert res_s_vi.status_code == 200
        assert res_s_vi.json()[0]["name"] == "Tốc Biến"

        res_s_en = await client.get("/api/v1/summoner-spells?locale=en_US")
        assert res_s_en.status_code == 200
        assert res_s_en.json()[0]["name"] == "Flash"
