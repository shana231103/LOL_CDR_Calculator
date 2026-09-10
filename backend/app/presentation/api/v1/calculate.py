# File: backend/app/presentation/api/v1/calculate.py

from fastapi import APIRouter, Depends
from app.infrastructure.di.container import get_calculate_cooldown_use_case
from app.application.use_cases.calculate_cooldown import CalculateCooldownUseCase
from app.application.dtos.calculate_dto import (
    CalculateCooldownCommand,
    RuneSelectionInputDTO,
)
from app.presentation.schemas.calculate_schema import (
    CalculateRequestSchema,
    CalculateResponseSchema,
    AbilityCooldownResponseSchema,
    SummonerCooldownResponseSchema,
)

router = APIRouter(prefix="/calculate", tags=["Calculation"])


@router.post("", response_model=CalculateResponseSchema)
async def calculate_cooldowns(
    request: CalculateRequestSchema,
    use_case: CalculateCooldownUseCase = Depends(get_calculate_cooldown_use_case),
) -> CalculateResponseSchema:
    command = CalculateCooldownCommand(
        champion_id=request.champion_id,
        abilities=request.abilities,
        items=request.items,
        runes=[
            RuneSelectionInputDTO(rune_id=r.rune_id, stacks=r.stacks)
            for r in request.runes
        ],
        summoner_spells=request.summoner_spells,
        locale=request.locale,
    )

    result_dto = await use_case.execute(command)

    abilities_resp = {
        slot: AbilityCooldownResponseSchema(
            slot=ab.slot,
            name=ab.name,
            rank=ab.rank,
            max_rank=ab.max_rank,
            base_cooldown=ab.base_cooldown,
            applicable_haste=ab.applicable_haste,
            final_cooldown=ab.final_cooldown,
            reduction_percentage=ab.reduction_percentage,
        )
        for slot, ab in result_dto.abilities.items()
    }

    spells_resp = [
        SummonerCooldownResponseSchema(
            id=s.id,
            name=s.name,
            base_cooldown=s.base_cooldown,
            applicable_haste=s.applicable_haste,
            final_cooldown=s.final_cooldown,
            reduction_percentage=s.reduction_percentage,
        )
        for s in result_dto.summoner_spells
    ]

    return CalculateResponseSchema(
        champion_id=result_dto.champion_id,
        ability_haste=result_dto.ability_haste,
        ultimate_haste=result_dto.ultimate_haste,
        summoner_haste=result_dto.summoner_haste,
        basic_haste=result_dto.basic_haste,
        abilities=abilities_resp,
        summoner_spells=spells_resp,
    )
