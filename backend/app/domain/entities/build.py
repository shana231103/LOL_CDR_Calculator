# File: backend/app/domain/entities/build.py

from dataclasses import dataclass, field
from app.domain.enums import SkillSlot, HasteType
from app.domain.value_objects import SkillRank, AbilityHaste
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import RuneSelection
from app.domain.entities.spell import SummonerSpell
from app.domain.exceptions import ItemLimitError, SpellLimitError, InvalidRankError


@dataclass
class Build:
    champion: Champion
    skill_ranks: dict[SkillSlot, SkillRank]
    items: list[Item] = field(default_factory=list)
    runes: list[RuneSelection] = field(default_factory=list)
    spells: list[SummonerSpell] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.validate_invariants()

    def validate_invariants(self) -> None:
        if len(self.items) > 6:
            raise ItemLimitError(f"A build cannot exceed 6 items, got {len(self.items)}.")
        if len(self.spells) > 2:
            raise SpellLimitError(f"A build cannot exceed 2 summoner spells, got {len(self.spells)}.")

        for slot, skill_rank in self.skill_ranks.items():
            if slot in self.champion.abilities:
                ability = self.champion.abilities[slot]
                if skill_rank.rank > ability.max_rank:
                    raise InvalidRankError(
                        f"Rank {skill_rank.rank} exceeds max rank {ability.max_rank} for ability {ability.name} ({slot.value})."
                    )

    def get_general_ability_haste(self) -> AbilityHaste:
        total = sum(item.ability_haste for item in self.items)
        for selection in self.runes:
            rtype, haste = selection.calculate_haste()
            if rtype == HasteType.ABILITY_HASTE:
                total += haste.value
        return AbilityHaste(total)

    def get_ultimate_haste(self) -> AbilityHaste:
        total = sum(item.ultimate_haste for item in self.items)
        for selection in self.runes:
            rtype, haste = selection.calculate_haste()
            if rtype == HasteType.ULTIMATE_HASTE:
                total += haste.value
        return AbilityHaste(total)

    def get_basic_ability_haste(self) -> AbilityHaste:
        total = sum(item.basic_haste for item in self.items)
        for selection in self.runes:
            rtype, haste = selection.calculate_haste()
            if rtype == HasteType.BASIC_HASTE:
                total += haste.value
        return AbilityHaste(total)

    def get_summoner_haste(self) -> AbilityHaste:
        total = sum(item.summoner_haste for item in self.items)
        for selection in self.runes:
            rtype, haste = selection.calculate_haste()
            if rtype == HasteType.SUMMONER_HASTE:
                total += haste.value
        return AbilityHaste(total)
