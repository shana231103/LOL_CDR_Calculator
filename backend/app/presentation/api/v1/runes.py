# File: backend/app/presentation/api/v1/runes.py

from fastapi import APIRouter, Depends
from app.infrastructure.di.container import get_runes_use_case
from app.application.use_cases.get_runes import GetRunesUseCase
from app.presentation.schemas.rune_schema import RuneResponseSchema

router = APIRouter(prefix="/runes", tags=["Runes"])


@router.get("", response_model=list[RuneResponseSchema])
async def list_runes(
    use_case: GetRunesUseCase = Depends(get_runes_use_case),
) -> list[RuneResponseSchema]:
    runes = await use_case.execute()
    return [
        RuneResponseSchema(
            id=r.id,
            key=r.key,
            name=r.name,
            icon_url=r.icon_url,
            haste_type=r.haste_type,
            base_haste=r.base_haste,
            haste_per_stack=r.haste_per_stack,
            max_stacks=r.max_stacks,
        )
        for r in runes
    ]
