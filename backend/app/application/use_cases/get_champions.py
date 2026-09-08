# File: backend/app/application/use_cases/get_champions.py

from app.domain.repositories.champion_repository import IChampionRepository
from app.application.dtos.champion_dto import ChampionDTO, AbilityDTO


def _map_champion_to_dto(champ) -> ChampionDTO:
    abilities = [
        AbilityDTO(
            id=ab.id,
            slot=ab.slot.value,
            name=ab.name,
            description=ab.description,
            image_url=ab.image_url,
            max_rank=ab.max_rank,
            cooldowns=ab.cooldowns,
        )
        for ab in champ.abilities.values()
    ]
    return ChampionDTO(
        id=champ.id,
        key=champ.key,
        name=champ.name,
        title=champ.title,
        image_url=champ.image_url,
        abilities=abilities,
    )


class GetChampionsUseCase:
    def __init__(self, champion_repo: IChampionRepository) -> None:
        self._champion_repo = champion_repo

    async def execute(self) -> list[ChampionDTO]:
        champions = await self._champion_repo.get_all()
        return [_map_champion_to_dto(c) for c in champions]


class GetChampionByIdUseCase:
    def __init__(self, champion_repo: IChampionRepository) -> None:
        self._champion_repo = champion_repo

    async def execute(self, champion_id: str) -> ChampionDTO | None:
        champion = await self._champion_repo.get_by_id(champion_id)
        if champion is None:
            return None
        return _map_champion_to_dto(champion)
