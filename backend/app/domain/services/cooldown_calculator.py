# File: backend/app/domain/services/cooldown_calculator.py

from typing import Any
from app.domain.enums import SkillSlot
from app.domain.value_objects import Cooldown, AbilityHaste
from app.domain.entities.build import Build


class CooldownCalculator:
    """Domain Service implementing pure algebraic League of Legends cooldown calculation."""

    @staticmethod
    def calculate_cooldown(base: Cooldown, haste: AbilityHaste) -> Cooldown:
        """Formula: Final = Base * 100 / (100 + Haste)"""
        if base.seconds <= 0.0:
            return Cooldown(0.0)
        final_secs = base.seconds * 100.0 / (100.0 + haste.value)
        return Cooldown(final_secs)

    @classmethod
    def calculate_build(cls, build: Build) -> dict[str, Any]:
        """Calculates cooldowns for abilities (Q/W/E/R) and summoner spells."""
        general_ah = build.get_general_ability_haste()
        ult_haste = build.get_ultimate_haste()
        basic_haste = build.get_basic_ability_haste()
        summoner_haste = build.get_summoner_haste()

        abilities_result: dict[str, dict[str, Any]] = {}
        for slot in [SkillSlot.Q, SkillSlot.W, SkillSlot.E, SkillSlot.R]:
            if slot not in build.champion.abilities:
                continue

            ability = build.champion.abilities[slot]
            skill_rank = build.skill_ranks.get(slot)
            rank_val = skill_rank.rank if skill_rank else 1
            base_cd = ability.get_cooldown_for_rank(rank_val)

            # Ultimate gets General AH + Ultimate Haste; Basic skills get General AH + Basic AH
            if slot == SkillSlot.R:
                total_ability_haste = general_ah + ult_haste
            else:
                total_ability_haste = general_ah + basic_haste

            final_cd = cls.calculate_cooldown(base_cd, total_ability_haste)
            cdr_pct = (
                ((base_cd.seconds - final_cd.seconds) / base_cd.seconds * 100.0)
                if base_cd.seconds > 0
                else 0.0
            )

            abilities_result[slot.value] = {
                "slot": slot.value,
                "name": ability.name,
                "rank": rank_val,
                "max_rank": ability.max_rank,
                "base_cooldown": base_cd.rounded,
                "applicable_haste": total_ability_haste.value,
                "final_cooldown": final_cd.rounded,
                "reduction_percentage": round(cdr_pct, 1),
            }

        spells_result: list[dict[str, Any]] = []
        for spell in build.spells:
            base_spell_cd = spell.get_base_cooldown()
            final_spell_cd = cls.calculate_cooldown(base_spell_cd, summoner_haste)
            cdr_pct = (
                ((base_spell_cd.seconds - final_spell_cd.seconds) / base_spell_cd.seconds * 100.0)
                if base_spell_cd.seconds > 0
                else 0.0
            )
            spells_result.append({
                "id": spell.id,
                "name": spell.name,
                "base_cooldown": base_spell_cd.rounded,
                "applicable_haste": summoner_haste.value,
                "final_cooldown": final_spell_cd.rounded,
                "reduction_percentage": round(cdr_pct, 1),
            })

        return {
            "champion_id": build.champion.id,
            "ability_haste": general_ah.value,
            "ultimate_haste": ult_haste.value,
            "basic_haste": basic_haste.value,
            "summoner_haste": summoner_haste.value,
            "abilities": abilities_result,
            "summoner_spells": spells_result,
        }
