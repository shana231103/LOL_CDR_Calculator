# File: backend/tests/unit/test_item_passive_haste.py

import pytest
from app.domain.enums import SkillSlot, HasteType
from app.domain.value_objects import SkillRank
from app.domain.entities.champion import Champion
from app.domain.entities.ability import Ability
from app.domain.entities.item import Item
from app.domain.entities.build import Build
from app.domain.entities.spell import SummonerSpell
from app.domain.services.cooldown_calculator import CooldownCalculator
from app.infrastructure.external.riot_client import RiotDataDragonClient


def test_parse_item_haste_descriptions():
    overlay = {
        "3050": {
            "name": "Zeke's Convergence",
            "ultimate_haste": 15.0,
        }
    }

    # 1. Malignance: 15 AH in stats + 20 Ultimate Ability Haste in passive
    malignance_desc = (
        "<mainText><stats><attention>90</attention> Ability Power<br>"
        "<attention>600</attention> Mana<br>"
        "<attention>15</attention> Ability Haste</stats><br><br>"
        "<passive>Scorn</passive><br>Gain 20 Ultimate Ability Haste.<br><br>"
        "<passive>Hatefog</passive><br>Damaging a champion...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(malignance_desc, 3118, overlay)
    assert ah == 15.0
    assert ult_h == 20.0
    assert basic_h == 0.0
    assert summ_h == 0.0

    # 2. Experimental Hexplate: 0 AH + 30 Ultimate Ability Haste in passive
    hexplate_desc = (
        "<mainText><stats><attention>40</attention> Attack Damage<br>"
        "<attention>450</attention> Health</stats><br><br>"
        "<passive>Hexcharged</passive><br>Gain 30 Ultimate Ability Haste.<br><br>"
        "<passive>Overdrive</passive><br>After casting your Ultimate...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(hexplate_desc, 3073, overlay)
    assert ah == 0.0
    assert ult_h == 30.0
    assert basic_h == 0.0
    assert summ_h == 0.0

    # 3. Fiendhunter Bolts: 0 AH + 30 Ultimate Ability Haste in passive
    fiendhunter_desc = (
        "<mainText><stats><attention>45%</attention> Attack Speed</stats><br><br>"
        "<passive>Night Vigil</passive><br>Gain 30 Ultimate Ability Haste.<br><br>"
        "<passive>Opening Barrage</passive><br>After casting...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(fiendhunter_desc, 2512, overlay)
    assert ah == 0.0
    assert ult_h == 30.0

    # 4. Zeke's Convergence: 10 AH in stats + 15 Ultimate Haste from overlay
    zeke_desc = (
        "<mainText><stats><attention>300</attention> Health<br>"
        "<attention>10</attention> Ability Haste</stats><br><br>"
        "<passive>Frostfire Tempest</passive><br>Casting your Ultimate...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(zeke_desc, 3050, overlay)
    assert ah == 10.0
    assert ult_h == 15.0

    # 5. Spear of Shojin: 0 AH + 25 Basic Ability Haste
    shojin_desc = (
        "<mainText><stats><attention>45</attention> Attack Damage</stats><br><br>"
        "<passive>Dragonforce</passive><br>Gain 25 Basic Ability Haste.<br><br>"
        "<passive>Focused Will</passive><br>Dealing damage...</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(shojin_desc, 3161, overlay)
    assert ah == 0.0
    assert ult_h == 0.0
    assert basic_h == 25.0

    # 6. Ionian Boots of Lucidity: 10 AH + 10 Summoner Spell Haste
    lucidity_desc = (
        "<mainText><stats><attention>10</attention> Ability Haste<br>"
        "<attention>45</attention> Move Speed</stats><br><br>"
        "Gain 10 Summoner Spell Haste.</mainText>"
    )
    ah, ult_h, basic_h, summ_h = RiotDataDragonClient._parse_item_haste(lucidity_desc, 3158, overlay)
    assert ah == 10.0
    assert summ_h == 10.0


def test_build_specialized_haste_aggregation():
    champ = Champion(id="Ahri", key="103", name="Ahri", title="Nine-Tailed Fox", image_url="")
    champ.add_ability(
        Ability(
            id="Ahri_R",
            slot=SkillSlot.R,
            name="Spirit Rush",
            description="",
            image_url="",
            max_rank=3,
            cooldowns=[130.0, 115.0, 100.0],
        )
    )
    champ.add_ability(
        Ability(
            id="Ahri_Q",
            slot=SkillSlot.Q,
            name="Orb of Deception",
            description="",
            image_url="",
            max_rank=5,
            cooldowns=[7.0, 7.0, 7.0, 7.0, 7.0],
        )
    )

    items = [
        Item(id=3118, name="Malignance", description="", image_url="", ability_haste=15.0, ultimate_haste=20.0),
        Item(id=3073, name="Experimental Hexplate", description="", image_url="", ability_haste=0.0, ultimate_haste=30.0),
        Item(id=3050, name="Zeke's Convergence", description="", image_url="", ability_haste=10.0, ultimate_haste=15.0),
        Item(id=3161, name="Spear of Shojin", description="", image_url="", ability_haste=0.0, basic_haste=25.0),
        Item(id=3158, name="Ionian Boots of Lucidity", description="", image_url="", ability_haste=10.0, summoner_haste=10.0),
    ]

    spells = [
        SummonerSpell(id="SummonerFlash", key="4", name="Flash", description="", cooldown=300.0, image_url=""),
    ]

    build = Build(
        champion=champ,
        skill_ranks={SkillSlot.R: SkillRank(rank=3, max_rank=3), SkillSlot.Q: SkillRank(rank=5, max_rank=5)},
        items=items,
        runes=[],
        spells=spells,
    )

    # General AH = 15 + 0 + 10 + 0 + 10 = 35.0
    assert build.get_general_ability_haste().value == 35.0
    # Ultimate Haste = 20 + 30 + 15 = 65.0
    assert build.get_ultimate_haste().value == 65.0
    # Basic Haste = 25.0
    assert build.get_basic_ability_haste().value == 25.0
    # Summoner Haste = 10.0
    assert build.get_summoner_haste().value == 10.0

    # Calculate Build
    res = CooldownCalculator.calculate_build(build)
    assert res["ability_haste"] == 35.0
    assert res["ultimate_haste"] == 65.0
    assert res["basic_haste"] == 25.0
    assert res["summoner_haste"] == 10.0

    # Slot R: Applicable Haste = 35 + 65 = 100.0 Haste -> 50% CDR -> Final CD = 50.0s (base 100.0s)
    r_res = res["abilities"]["R"]
    assert r_res["applicable_haste"] == 100.0
    assert r_res["final_cooldown"] == 50.0
    assert r_res["reduction_percentage"] == 50.0

    # Slot Q: Applicable Haste = 35 (General) + 25 (Basic) = 60.0 Haste
    q_res = res["abilities"]["Q"]
    assert q_res["applicable_haste"] == 60.0
    # Final CD = 7.0 * 100 / 160 = 4.375 -> rounded to 4.38s
    assert q_res["final_cooldown"] == 4.38

    # Flash: Applicable Haste = 10.0 -> Final CD = 300 * 100 / 110 = 272.73s
    flash_res = res["summoner_spells"][0]
    assert flash_res["applicable_haste"] == 10.0
    assert flash_res["final_cooldown"] == 272.73
