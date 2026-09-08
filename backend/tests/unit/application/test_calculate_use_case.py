# File: backend/tests/unit/application/test_calculate_use_case.py

import pytest
from app.domain.enums import SkillSlot, HasteType
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell
from app.domain.repositories.champion_repository import IChampionRepository
from app.domain.repositories.item_repository import IItemRepository
from app.domain.repositories.rune_repository import IRuneRepository
from app.domain.repositories.spell_repository import ISpellRepository
from app.domain.exceptions import EntityNotFoundError
from app.application.dtos.calculate_dto import (
    CalculateCooldownCommand,
    RuneSelectionInputDTO,
)
from app.application.use_cases.calculate_cooldown import CalculateCooldownUseCase


class InMemoryChampionRepo(IChampionRepository):
    def __init__(self, champions: list[Champion]) -> None:
        self._champions = {c.id: c for c in champions}

    async def get_all(self) -> list[Champion]:
        return list(self._champions.values())

    async def get_by_id(self, champion_id: str) -> Champion | None:
        return self._champions.get(champion_id)

    async def upsert_many(self, champions: list[Champion]) -> None:
        for c in champions:
            self._champions[c.id] = c


class InMemoryItemRepo(IItemRepository):
    def __init__(self, items: list[Item]) -> None:
        self._items = {i.id: i for i in items}

    async def get_all(self, search: str | None = None) -> list[Item]:
        return list(self._items.values())

    async def get_by_ids(self, item_ids: list[int]) -> list[Item]:
        return [self._items[i] for i in item_ids if i in self._items]

    async def upsert_many(self, items: list[Item]) -> None:
        for i in items:
            self._items[i.id] = i

    async def delete_all(self) -> None:
        self._items.clear()



class InMemoryRuneRepo(IRuneRepository):
    def __init__(self, runes: list[Rune]) -> None:
        self._runes = {r.id: r for r in runes}

    async def get_haste_runes(self) -> list[Rune]:
        return list(self._runes.values())

    async def get_by_ids(self, rune_ids: list[int]) -> list[Rune]:
        return [self._runes[r] for r in rune_ids if r in self._runes]

    async def upsert_many(self, runes: list[Rune]) -> None:
        for r in runes:
            self._runes[r.id] = r


class InMemorySpellRepo(ISpellRepository):
    def __init__(self, spells: list[SummonerSpell]) -> None:
        self._spells = {s.id: s for s in spells}

    async def get_all(self) -> list[SummonerSpell]:
        return list(self._spells.values())

    async def get_by_ids(self, spell_ids: list[str]) -> list[SummonerSpell]:
        return [self._spells[s] for s in spell_ids if s in self._spells]

    async def upsert_many(self, spells: list[SummonerSpell]) -> None:
        for s in spells:
            self._spells[s.id] = s


@pytest.mark.anyio
async def test_calculate_use_case_success():
    champ = Champion(id="Lux", key="99", name="Lux", title="Lady of Luminosity", image_url="")
    champ.add_ability(
        Ability(
            id="LuxR",
            slot=SkillSlot.R,
            name="Final Spark",
            description="Laser",
            image_url="",
            max_rank=3,
            cooldowns=[80.0, 60.0, 40.0],
        )
    )
    item = Item(id=3157, name="Zhonya", description="", image_url="", ability_haste=15.0)
    rune = Rune(
        id=8106,
        key="UltimateHunter",
        name="Ultimate Hunter",
        icon_url="",
        haste_type=HasteType.ULTIMATE_HASTE,
        base_haste=6.0,
        haste_per_stack=5.0,
        max_stacks=5,
    )
    spell = SummonerSpell(id="SummonerFlash", key="4", name="Flash", description="", cooldown=300.0, image_url="")

    c_repo = InMemoryChampionRepo([champ])
    i_repo = InMemoryItemRepo([item])
    r_repo = InMemoryRuneRepo([rune])
    s_repo = InMemorySpellRepo([spell])

    use_case = CalculateCooldownUseCase(c_repo, i_repo, r_repo, s_repo)

    command = CalculateCooldownCommand(
        champion_id="Lux",
        abilities={"R": 2},  # Base CD = 60.0s
        items=[3157],       # 15 AH
        runes=[RuneSelectionInputDTO(rune_id=8106, stacks=2)],  # 6 + 10 = 16 Ult Haste
        summoner_spells=["SummonerFlash"],
    )

    result = await use_case.execute(command)

    assert result.champion_id == "Lux"
    assert result.ability_haste == 15.0
    assert result.ultimate_haste == 16.0
    # R gets 15 + 16 = 31 AH. Final = 60 * 100 / 131 = 45.80s
    assert result.abilities["R"].final_cooldown == 45.8
    assert result.abilities["R"].rank == 2
    assert len(result.summoner_spells) == 1


@pytest.mark.anyio
async def test_calculate_use_case_champion_not_found():
    c_repo = InMemoryChampionRepo([])
    i_repo = InMemoryItemRepo([])
    r_repo = InMemoryRuneRepo([])
    s_repo = InMemorySpellRepo([])

    use_case = CalculateCooldownUseCase(c_repo, i_repo, r_repo, s_repo)
    command = CalculateCooldownCommand(champion_id="Unknown")

    with pytest.raises(EntityNotFoundError):
        await use_case.execute(command)


@pytest.mark.anyio
async def test_calculate_use_case_specialized_item_haste():
    lux = Champion(
        id="Lux",
        key="99",
        name="Lux",
        title="the Lady of Luminosity",
        image_url="lux.png",
    )
    lux.add_ability(
        Ability(
            id="Lux_R",
            slot=SkillSlot.R,
            name="Final Spark",
            description="",
            image_url="",
            max_rank=3,
            cooldowns=[80.0, 60.0, 40.0],
        )
    )
    lux.add_ability(
        Ability(
            id="Lux_Q",
            slot=SkillSlot.Q,
            name="Light Binding",
            description="",
            image_url="",
            max_rank=5,
            cooldowns=[11.0, 10.5, 10.0, 9.5, 9.0],
        )
    )

    items = [
        Item(id=3118, name="Malignance", description="", image_url="", ability_haste=15.0, ultimate_haste=20.0),
        Item(id=3073, name="Experimental Hexplate", description="", image_url="", ability_haste=0.0, ultimate_haste=30.0),
        Item(id=3050, name="Zeke's Convergence", description="", image_url="", ability_haste=10.0, ultimate_haste=15.0),
        Item(id=3161, name="Spear of Shojin", description="", image_url="", ability_haste=0.0, basic_haste=25.0),
    ]

    use_case = CalculateCooldownUseCase(
        InMemoryChampionRepo([lux]),
        InMemoryItemRepo(items),
        InMemoryRuneRepo([]),
        InMemorySpellRepo([]),
    )

    command = CalculateCooldownCommand(
        champion_id="Lux",
        abilities={"R": 3, "Q": 5},
        items=[3118, 3073, 3050, 3161],
        runes=[],
        summoner_spells=[],
    )

    result = await use_case.execute(command)
    assert result.ability_haste == 25.0  # 15 + 10
    assert result.ultimate_haste == 65.0  # 20 + 30 + 15
    assert result.basic_haste == 25.0

    # R: 25 AH + 65 Ult Haste = 90 Haste. Base CD rank 3 = 40.0s -> 40 * 100 / 190 = 21.05s
    assert result.abilities["R"].applicable_haste == 90.0
    assert result.abilities["R"].final_cooldown == 21.05

    # Q: 25 AH + 25 Basic Haste = 50 Haste. Base CD rank 5 = 9.0s -> 9 * 100 / 150 = 6.0s
    assert result.abilities["Q"].applicable_haste == 50.0
    assert result.abilities["Q"].final_cooldown == 6.0
