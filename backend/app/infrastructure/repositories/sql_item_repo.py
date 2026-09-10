# File: backend/app/infrastructure/repositories/sql_item_repo.py

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.item import Item
from app.domain.repositories.item_repository import IItemRepository
from app.infrastructure.database.models.item_orm import ItemORM


def _orm_to_domain(orm: ItemORM) -> Item:
    return Item(
        id=orm.id,
        name=orm.name,
        description=orm.description,
        image_url=orm.image_url,
        ability_haste=float(orm.ability_haste or 0.0),
        ultimate_haste=float(orm.ultimate_haste or 0.0),
        basic_haste=float(orm.basic_haste or 0.0),
        summoner_haste=float(orm.summoner_haste or 0.0),
        gold_total=orm.gold_total,
        locale=orm.locale,
    )


class SqlItemRepository(IItemRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, search: str | None = None, locale: str = "vi_VN") -> list[Item]:
        stmt = select(ItemORM).where(ItemORM.locale == locale)
        if search and search.strip():
            stmt = stmt.where(ItemORM.name.ilike(f"%{search.strip()}%"))
        stmt = stmt.order_by(ItemORM.name)
        res = await self._session.execute(stmt)
        return [_orm_to_domain(i) for i in res.scalars().all()]

    async def get_by_ids(self, item_ids: list[int], locale: str | None = None) -> list[Item]:
        if not item_ids:
            return []
        stmt = select(ItemORM).where(ItemORM.id.in_(item_ids))
        if locale:
            stmt = stmt.where(ItemORM.locale == locale)
        res = await self._session.execute(stmt)
        return [_orm_to_domain(i) for i in res.scalars().all()]

    async def upsert_many(self, items: list[Item], locale: str = "vi_VN") -> None:
        for it in items:
            loc = getattr(it, "locale", locale) or locale
            existing = await self._session.get(ItemORM, (it.id, loc))
            if existing:
                existing.name = it.name
                existing.description = it.description
                existing.image_url = it.image_url
                existing.ability_haste = it.ability_haste
                existing.ultimate_haste = it.ultimate_haste
                existing.basic_haste = it.basic_haste
                existing.summoner_haste = it.summoner_haste
                existing.gold_total = it.gold_total
            else:
                self._session.add(
                    ItemORM(
                        id=it.id,
                        locale=loc,
                        name=it.name,
                        description=it.description,
                        image_url=it.image_url,
                        ability_haste=it.ability_haste,
                        ultimate_haste=it.ultimate_haste,
                        basic_haste=it.basic_haste,
                        summoner_haste=it.summoner_haste,
                        gold_total=it.gold_total,
                    )
                )
        await self._session.flush()

    async def delete_all(self, locale: str | None = None) -> None:
        stmt = delete(ItemORM)
        if locale:
            stmt = stmt.where(ItemORM.locale == locale)
        await self._session.execute(stmt)
        await self._session.flush()
