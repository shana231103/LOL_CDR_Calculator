# File: backend/app/infrastructure/repositories/sql_champion_repo.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.enums import SkillSlot
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.repositories.champion_repository import IChampionRepository
from app.infrastructure.database.models.champion_orm import ChampionORM
from app.infrastructure.database.models.ability_orm import AbilityORM


def _orm_to_domain(orm: ChampionORM) -> Champion:
    champ = Champion(
        id=orm.id,
        key=orm.key,
        name=orm.name,
        title=orm.title,
        image_url=orm.image_url,
        locale=orm.locale,
    )
    for ab in orm.abilities:
        slot = SkillSlot(ab.slot)
        champ.add_ability(
            Ability(
                id=ab.id,
                slot=slot,
                name=ab.name,
                description=ab.description,
                image_url=ab.image_url,
                max_rank=ab.max_rank,
                cooldowns=list(ab.cooldowns or []),
            )
        )
    return champ


class SqlChampionRepository(IChampionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, locale: str = "vi_VN") -> list[Champion]:
        stmt = select(ChampionORM).where(ChampionORM.locale == locale).order_by(ChampionORM.name)
        res = await self._session.execute(stmt)
        return [_orm_to_domain(c) for c in res.scalars().all()]

    async def get_by_id(self, champion_id: str, locale: str | None = None) -> Champion | None:
        stmt = select(ChampionORM).where(ChampionORM.id == champion_id)
        if locale:
            stmt = stmt.where(ChampionORM.locale == locale)
        res = await self._session.execute(stmt)
        orm = res.scalars().first()
        return _orm_to_domain(orm) if orm else None

    async def upsert_many(self, champions: list[Champion], locale: str = "vi_VN") -> None:
        for champ in champions:
            loc = getattr(champ, "locale", locale) or locale
            existing = await self._session.get(ChampionORM, (champ.id, loc))
            if existing:
                existing.key = champ.key
                existing.name = champ.name
                existing.title = champ.title
                existing.image_url = champ.image_url
                existing.abilities.clear()
                for ab in champ.abilities.values():
                    existing.abilities.append(
                        AbilityORM(
                            id=ab.id,
                            locale=loc,
                            champion_id=champ.id,
                            slot=ab.slot.value,
                            name=ab.name,
                            description=ab.description,
                            image_url=ab.image_url,
                            max_rank=ab.max_rank,
                            cooldowns=ab.cooldowns,
                        )
                    )
            else:
                new_orm = ChampionORM(
                    id=champ.id,
                    locale=loc,
                    key=champ.key,
                    name=champ.name,
                    title=champ.title,
                    image_url=champ.image_url,
                )
                for ab in champ.abilities.values():
                    new_orm.abilities.append(
                        AbilityORM(
                            id=ab.id,
                            locale=loc,
                            champion_id=champ.id,
                            slot=ab.slot.value,
                            name=ab.name,
                            description=ab.description,
                            image_url=ab.image_url,
                            max_rank=ab.max_rank,
                            cooldowns=ab.cooldowns,
                        )
                    )
                self._session.add(new_orm)
        await self._session.flush()
