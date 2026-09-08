# File: backend/tests/unit/domain/test_build_aggregate.py

import pytest
from app.domain.enums import SkillSlot, HasteType
from app.domain.value_objects import Cooldown, AbilityHaste, SkillRank
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune, RuneSelection
from app.domain.entities.spell import SummonerSpell
from app.domain.entities.build import Build
from app.domain.exceptions import (
    ItemLimitError,
    SpellLimitError,
    InvalidRankError,
    InvalidHasteError,
    DomainError,
)


def create_sample_champion():
    champ = Champion(
        id="Ahri",
        key="103",
        name="Ahri",
        title="the Nine-Tailed Fox",
        image_url="http://cdn/Ahri.png",
    )
    champ.add_ability(
        Ability(
            id="AhriQ",
            slot=SkillSlot.Q,
            name="Orb of Deception",
            description="Orb",
            image_url="http://cdn/AhriQ.png",
            max_rank=5,
            cooldowns=[7.0, 7.0, 7.0, 7.0, 7.0],
        )
    )
    return champ


def test_build_rejects_more_than_6_items():
    champ = create_sample_champion()
    items = [
        Item(id=i, name=f"Item {i}", description="", image_url="", ability_haste=10)
        for i in range(7)
    ]
    with pytest.raises(ItemLimitError):
        Build(
            champion=champ,
            skill_ranks={SkillSlot.Q: SkillRank(rank=1, max_rank=5)},
            items=items,
        )


def test_build_rejects_more_than_2_spells():
    champ = create_sample_champion()
    spells = [
        SummonerSpell(id=f"S{i}", key=str(i), name=f"Spell {i}", description="", cooldown=100.0, image_url="")
        for i in range(3)
    ]
    with pytest.raises(SpellLimitError):
        Build(
            champion=champ,
            skill_ranks={SkillSlot.Q: SkillRank(rank=1, max_rank=5)},
            spells=spells,
        )


def test_build_rejects_rank_exceeding_max_rank():
    champ = create_sample_champion()
    with pytest.raises(InvalidRankError):
        Build(
            champion=champ,
            skill_ranks={SkillSlot.Q: SkillRank(rank=6, max_rank=6)},  # max_rank is 5 in champ
        )


def test_value_object_negative_validation():
    with pytest.raises(InvalidHasteError):
        Cooldown(-5.0)

    with pytest.raises(InvalidHasteError):
        AbilityHaste(-10.0)

    with pytest.raises(InvalidRankError):
        SkillRank(rank=0, max_rank=5)


def test_rune_stack_exceeding_limit():
    rune = Rune(
        id=8106,
        key="UltimateHunter",
        name="Ultimate Hunter",
        icon_url="http://cdn/rune.png",
        haste_type=HasteType.ULTIMATE_HASTE,
        base_haste=6.0,
        haste_per_stack=5.0,
        max_stacks=5,
    )
    with pytest.raises(DomainError):
        RuneSelection(rune=rune, stacks=6)
