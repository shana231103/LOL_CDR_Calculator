# File: backend/app/presentation/api/v1/champions.py

from fastapi import APIRouter, Depends, HTTPException, Query
from app.infrastructure.di.container import (
    get_champions_use_case,
    get_champion_by_id_use_case,
)
from app.application.use_cases.get_champions import (
    GetChampionsUseCase,
    GetChampionByIdUseCase,
)
from app.presentation.schemas.champion_schema import (
    ChampionResponseSchema,
    AbilityResponseSchema,
)

router = APIRouter(prefix="/champions", tags=["Champions"])


@router.get("", response_model=list[ChampionResponseSchema])
async def list_champions(
    locale: str = Query("vi_VN", pattern="^(vi_VN|en_US)$"),
    use_case: GetChampionsUseCase = Depends(get_champions_use_case),
) -> list[ChampionResponseSchema]:
    champions = await use_case.execute(locale=locale)
    return [
        ChampionResponseSchema(
            id=c.id,
            key=c.key,
            name=c.name,
            title=c.title,
            image_url=c.image_url,
            abilities=[
                AbilityResponseSchema(
                    id=ab.id,
                    slot=ab.slot,
                    name=ab.name,
                    description=ab.description,
                    image_url=ab.image_url,
                    max_rank=ab.max_rank,
                    cooldowns=ab.cooldowns,
                )
                for ab in c.abilities
            ],
        )
        for c in champions
    ]


@router.get("/{champion_id}", response_model=ChampionResponseSchema)
async def get_champion(
    champion_id: str,
    locale: str = Query("vi_VN", pattern="^(vi_VN|en_US)$"),
    use_case: GetChampionByIdUseCase = Depends(get_champion_by_id_use_case),
) -> ChampionResponseSchema:
    champ = await use_case.execute(champion_id, locale=locale)
    if champ is None:
        raise HTTPException(
            status_code=404,
            detail=f"Champion '{champion_id}' not found.",
        )
    return ChampionResponseSchema(
        id=champ.id,
        key=champ.key,
        name=champ.name,
        title=champ.title,
        image_url=champ.image_url,
        abilities=[
            AbilityResponseSchema(
                id=ab.id,
                slot=ab.slot,
                name=ab.name,
                description=ab.description,
                image_url=ab.image_url,
                max_rank=ab.max_rank,
                cooldowns=ab.cooldowns,
            )
            for ab in champ.abilities
        ],
    )
