# File: backend/app/presentation/api/v1/spells.py

from fastapi import APIRouter, Depends
from app.infrastructure.di.container import get_spells_use_case
from app.application.use_cases.get_spells import GetSpellsUseCase
from app.presentation.schemas.spell_schema import SpellResponseSchema

router = APIRouter(prefix="/summoner-spells", tags=["Summoner Spells"])


@router.get("", response_model=list[SpellResponseSchema])
async def list_spells(
    use_case: GetSpellsUseCase = Depends(get_spells_use_case),
) -> list[SpellResponseSchema]:
    spells = await use_case.execute()
    return [
        SpellResponseSchema(
            id=s.id,
            key=s.key,
            name=s.name,
            description=s.description,
            cooldown=s.cooldown,
            image_url=s.image_url,
        )
        for s in spells
    ]
