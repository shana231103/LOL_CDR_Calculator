# File: backend/app/infrastructure/repositories/sql_rune_repo.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.enums import HasteType
from app.domain.entities.rune import Rune
from app.domain.repositories.rune_repository import IRuneRepository
from app.infrastructure.database.models.rune_orm import RuneORM


def _orm_to_domain(orm: RuneORM) -> Rune:
    return Rune(
        id=orm.id,
        key=orm.key,
        name=orm.name,
        icon_url=orm.icon_url,
        haste_type=HasteType(orm.haste_type),
        base_haste=orm.base_haste,
        haste_per_stack=orm.haste_per_stack,
        max_stacks=orm.max_stacks,
    )


class SqlRuneRepository(IRuneRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_haste_runes(self) -> list[Rune]:
        stmt = select(RuneORM).order_by(RuneORM.name)
        res = await self._session.execute(stmt)
        return [_orm_to_domain(r) for r in res.scalars().all()]

    async def get_by_ids(self, rune_ids: list[int]) -> list[Rune]:
        if not rune_ids:
            return []
        stmt = select(RuneORM).where(RuneORM.id.in_(rune_ids))
        res = await self._session.execute(stmt)
        return [_orm_to_domain(r) for r in res.scalars().all()]

    async def upsert_many(self, runes: list[Rune]) -> None:
        for r in runes:
            existing = await self._session.get(RuneORM, r.id)
            if existing:
                existing.key = r.key
                existing.name = r.name
                existing.icon_url = r.icon_url
                existing.haste_type = r.haste_type.value
                existing.base_haste = r.base_haste
                existing.haste_per_stack = r.haste_per_stack
                existing.max_stacks = r.max_stacks
            else:
                self._session.add(
                    RuneORM(
                        id=r.id,
                        key=r.key,
                        name=r.name,
                        icon_url=r.icon_url,
                        haste_type=r.haste_type.value,
                        base_haste=r.base_haste,
                        haste_per_stack=r.haste_per_stack,
                        max_stacks=r.max_stacks,
                    )
                )
        await self._session.flush()
