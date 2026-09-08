# File: backend/app/application/dtos/champion_dto.py

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AbilityDTO:
    id: str
    slot: str
    name: str
    description: str
    image_url: str
    max_rank: int
    cooldowns: list[float]


@dataclass(frozen=True)
class ChampionDTO:
    id: str
    key: str
    name: str
    title: str
    image_url: str
    abilities: list[AbilityDTO] = field(default_factory=list)
