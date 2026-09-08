# File: backend/app/application/use_cases/calculate_cooldown.py

from app.domain.enums import SkillSlot
from app.domain.value_objects import SkillRank
from app.domain.entities.rune import RuneSelection
from app.domain.entities.build import Build
from app.domain.services.cooldown_calculator import CooldownCalculator
from app.domain.repositories.champion_repository import IChampionRepository
from app.domain.repositories.item_repository import IItemRepository
from app.domain.repositories.rune_repository import IRuneRepository
from app.domain.repositories.spell_repository import ISpellRepository
from app.domain.exceptions import EntityNotFoundError
from app.application.dtos.calculate_dto import (
    CalculateCooldownCommand,
    CalculationResultDTO,
    AbilityCooldownResultDTO,
    SummonerCooldownResultDTO,
)


class CalculateCooldownUseCase:
    """Use Case: Orchestrates domain repositories and CooldownCalculator service."""

    def __init__(
        self,
        champion_repo: IChampionRepository,
        item_repo: IItemRepository,
        rune_repo: IRuneRepository,
        spell_repo: ISpellRepository,
    ) -> None:
        self._champion_repo = champion_repo
        self._item_repo = item_repo
        self._rune_repo = rune_repo
        self._spell_repo = spell_repo

    async def execute(self, command: CalculateCooldownCommand) -> CalculationResultDTO:
        champion = await self._champion_repo.get_by_id(command.champion_id)
        if champion is None:
            raise EntityNotFoundError(f"Champion '{command.champion_id}' not found.")

        # Load items
        items = await self._item_repo.get_by_ids(command.items) if command.items else []

        # Load runes and construct RuneSelections
        rune_ids = [r.rune_id for r in command.runes]
        loaded_runes = await self._rune_repo.get_by_ids(rune_ids) if rune_ids else []
        runes_map = {r.id: r for r in loaded_runes}
        rune_selections: list[RuneSelection] = []
        for r_input in command.runes:
            if r_input.rune_id in runes_map:
                rune_selections.append(
                    RuneSelection(rune=runes_map[r_input.rune_id], stacks=r_input.stacks)
                )

        # Load summoner spells
        spells = (
            await self._spell_repo.get_by_ids(command.summoner_spells)
            if command.summoner_spells
            else []
        )

        # Build skill ranks
        skill_ranks: dict[SkillSlot, SkillRank] = {}
        for slot in [SkillSlot.Q, SkillSlot.W, SkillSlot.E, SkillSlot.R]:
            if slot in champion.abilities:
                ability = champion.abilities[slot]
                rank_val = command.abilities.get(slot.value, 1)
                skill_ranks[slot] = SkillRank(rank=rank_val, max_rank=ability.max_rank)

        # Construct and validate Domain Aggregate Root
        build = Build(
            champion=champion,
            skill_ranks=skill_ranks,
            items=items,
            runes=rune_selections,
            spells=spells,
        )

        # Execute pure domain calculation
        calc_result = CooldownCalculator.calculate_build(build)

        # Map to Output DTO
        abilities_dto: dict[str, AbilityCooldownResultDTO] = {}
        for slot_str, data in calc_result["abilities"].items():
            abilities_dto[slot_str] = AbilityCooldownResultDTO(
                slot=data["slot"],
                name=data["name"],
                rank=data["rank"],
                max_rank=data["max_rank"],
                base_cooldown=data["base_cooldown"],
                applicable_haste=data["applicable_haste"],
                final_cooldown=data["final_cooldown"],
                reduction_percentage=data["reduction_percentage"],
            )

        spells_dto: list[SummonerCooldownResultDTO] = [
            SummonerCooldownResultDTO(
                id=s["id"],
                name=s["name"],
                base_cooldown=s["base_cooldown"],
                applicable_haste=s["applicable_haste"],
                final_cooldown=s["final_cooldown"],
                reduction_percentage=s["reduction_percentage"],
            )
            for s in calc_result["summoner_spells"]
        ]

        return CalculationResultDTO(
            champion_id=calc_result["champion_id"],
            ability_haste=calc_result["ability_haste"],
            ultimate_haste=calc_result["ultimate_haste"],
            summoner_haste=calc_result["summoner_haste"],
            abilities=abilities_dto,
            summoner_spells=spells_dto,
            basic_haste=calc_result.get("basic_haste", 0.0),
        )
