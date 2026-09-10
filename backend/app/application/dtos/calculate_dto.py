# File: backend/app/application/dtos/calculate_dto.py

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RuneSelectionInputDTO:
    rune_id: int
    stacks: int = 0


@dataclass(frozen=True)
class CalculateCooldownCommand:
    champion_id: str
    abilities: dict[str, int] = field(default_factory=dict)
    items: list[int] = field(default_factory=list)
    runes: list[RuneSelectionInputDTO] = field(default_factory=list)
    summoner_spells: list[str] = field(default_factory=list)
    locale: str = "vi_VN"


@dataclass(frozen=True)
class AbilityCooldownResultDTO:
    slot: str
    name: str
    rank: int
    max_rank: int
    base_cooldown: float
    applicable_haste: float
    final_cooldown: float
    reduction_percentage: float


@dataclass(frozen=True)
class SummonerCooldownResultDTO:
    id: str
    name: str
    base_cooldown: float
    applicable_haste: float
    final_cooldown: float
    reduction_percentage: float


@dataclass(frozen=True)
class CalculationResultDTO:
    champion_id: str
    ability_haste: float
    ultimate_haste: float
    summoner_haste: float
    abilities: dict[str, AbilityCooldownResultDTO]
    summoner_spells: list[SummonerCooldownResultDTO]
    basic_haste: float = 0.0
