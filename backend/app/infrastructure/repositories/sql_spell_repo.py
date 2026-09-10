# File: backend/app/infrastructure/repositories/sql_spell_repo.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.spell import SummonerSpell
from app.domain.repositories.spell_repository import ISpellRepository
from app.infrastructure.database.models.spell_orm import SpellORM


def _orm_to_domain(orm: SpellORM) -> SummonerSpell:
    return SummonerSpell(
        id=orm.id,
        key=orm.key,
        name=orm.name,
        description=orm.description,
        cooldown=orm.cooldown,
        image_url=orm.image_url,
        locale=orm.locale,
    )


class SqlSpellRepository(ISpellRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, locale: str = "vi_VN") -> list[SummonerSpell]:
        stmt = select(SpellORM).where(SpellORM.locale == locale).order_by(SpellORM.name)
        res = await self._session.execute(stmt)
        return [_orm_to_domain(s) for s in res.scalars().all()]

    async def get_by_ids(self, spell_ids: list[str], locale: str | None = None) -> list[SummonerSpell]:
        if not spell_ids:
            return []
        stmt = select(SpellORM).where(SpellORM.id.in_(spell_ids))
        if locale:
            stmt = stmt.where(SpellORM.locale == locale)
        res = await self._session.execute(stmt)
        return [_orm_to_domain(s) for s in res.scalars().all()]

    async def upsert_many(self, spells: list[SummonerSpell], locale: str = "vi_VN") -> None:
        for s in spells:
            loc = getattr(s, "locale", locale) or locale
            existing = await self._session.get(SpellORM, (s.id, loc))
            if existing:
                existing.key = s.key
                existing.name = s.name
                existing.description = s.description
                existing.cooldown = s.cooldown
                existing.image_url = s.image_url
            else:
                self._session.add(
                    SpellORM(
                        id=s.id,
                        locale=loc,
                        key=s.key,
                        name=s.name,
                        description=s.description,
                        cooldown=s.cooldown,
                        image_url=s.image_url,
                    )
                )
        await self._session.flush()
