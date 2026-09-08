# File: backend/tests/unit/domain/test_cooldown_calculator.py

import pytest
from app.domain.enums import SkillSlot, HasteType
from app.domain.value_objects import Cooldown, AbilityHaste, SkillRank
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune, RuneSelection
from app.domain.entities.spell import SummonerSpell
from app.domain.entities.build import Build
from app.domain.services.cooldown_calculator import CooldownCalculator


def test_calculate_cooldown_formula():
    base = Cooldown(100.0)
    haste = AbilityHaste(100.0)
    result = CooldownCalculator.calculate_cooldown(base, haste)
    assert result.rounded == 50.0

    base2 = Cooldown(10.0)
    haste2 = AbilityHaste(25.0)
    result2 = CooldownCalculator.calculate_cooldown(base2, haste2)
    assert result2.rounded == 8.0


def test_calculate_cooldown_zero():
    base = Cooldown(0.0)
    haste = AbilityHaste(50.0)
    result = CooldownCalculator.calculate_cooldown(base, haste)
    assert result.rounded == 0.0


def test_calculate_build_separation_of_haste():
    # Champion with Q and R
    q_ability = Ability(
        id="AhriQ",
        slot=SkillSlot.Q,
        name="Orb of Deception",
        description="Throws orb",
        image_url="http://cdn/AhriQ.png",
        max_rank=5,
        cooldowns=[7.0, 7.0, 7.0, 7.0, 7.0],
    )
    r_ability = Ability(
        id="AhriR",
        slot=SkillSlot.R,
        name="Spirit Rush",
        description="Dashes",
        image_url="http://cdn/AhriR.png",
        max_rank=3,
        cooldowns=[130.0, 105.0, 80.0],
    )
    champ = Champion(
        id="Ahri",
        key="103",
        name="Ahri",
        title="the Nine-Tailed Fox",
        image_url="http://cdn/Ahri.png",
    )
    champ.add_ability(q_ability)
    champ.add_ability(r_ability)

    # Item with 25 AH
    item = Item(
        id=3001,
        name="Haste Item",
        description="Gives AH",
        image_url="http://cdn/item.png",
        ability_haste=25.0,
    )

    # Rune: Ultimate Hunter (6 base + 5 per stack, 3 stacks = 21 Ult Haste)
    ult_hunter = Rune(
        id=8106,
        key="UltimateHunter",
        name="Ultimate Hunter",
        icon_url="http://cdn/rune.png",
        haste_type=HasteType.ULTIMATE_HASTE,
        base_haste=6.0,
        haste_per_stack=5.0,
        max_stacks=5,
    )
    rune_sel = RuneSelection(rune=ult_hunter, stacks=3)

    # Spell: Flash (300s)
    flash = SummonerSpell(
        id="SummonerFlash",
        key="4",
        name="Flash",
        description="Teleport",
        cooldown=300.0,
        image_url="http://cdn/flash.png",
    )

    build = Build(
        champion=champ,
        skill_ranks={
            SkillSlot.Q: SkillRank(rank=5, max_rank=5),
            SkillSlot.R: SkillRank(rank=1, max_rank=3),
        },
        items=[item],
        runes=[rune_sel],
        spells=[flash],
    )

    res = CooldownCalculator.calculate_build(build)

    assert res["ability_haste"] == 25.0
    assert res["ultimate_haste"] == 21.0
    # Q only gets General AH (25): 7.0 * 100 / 125 = 5.6s
    assert res["abilities"]["Q"]["final_cooldown"] == 5.6
    # R gets General AH (25) + Ult Haste (21) = 46 AH: 130 * 100 / 146 = 89.04s
    assert res["abilities"]["R"]["applicable_haste"] == 46.0
    assert res["abilities"]["R"]["final_cooldown"] == 89.04
    # Flash gets 0 summoner haste = 300.0s
    assert res["summoner_spells"][0]["final_cooldown"] == 300.0
