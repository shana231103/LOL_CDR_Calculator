# File: backend/app/presentation/schemas/calculate_schema.py

from pydantic import BaseModel, Field


class RuneSelectionSchema(BaseModel):
    rune_id: int
    stacks: int = Field(default=0, ge=0, le=10)


class CalculateRequestSchema(BaseModel):
    champion_id: str = Field(..., min_length=1, description="Champion identifier e.g. 'Ahri'")
    abilities: dict[str, int] = Field(
        default_factory=lambda: {"Q": 1, "W": 1, "E": 1, "R": 1},
        description="Dictionary mapping slot (Q, W, E, R) to rank",
    )
    items: list[int] = Field(
        default_factory=list,
        max_length=6,
        description="Array of item IDs up to 6 items",
    )
    runes: list[RuneSelectionSchema] = Field(
        default_factory=list,
        description="Selected runes with stack count",
    )
    summoner_spells: list[str] = Field(
        default_factory=list,
        max_length=2,
        description="Array of summoner spell IDs up to 2 spells",
    )
    locale: str = Field(
        default="vi_VN",
        description="Locale for calculation entities e.g. 'vi_VN' or 'en_US'",
    )


class AbilityCooldownResponseSchema(BaseModel):
    slot: str
    name: str
    rank: int
    max_rank: int
    base_cooldown: float
    applicable_haste: float
    final_cooldown: float
    reduction_percentage: float


class SummonerCooldownResponseSchema(BaseModel):
    id: str
    name: str
    base_cooldown: float
    applicable_haste: float
    final_cooldown: float
    reduction_percentage: float


class CalculateResponseSchema(BaseModel):
    champion_id: str
    ability_haste: float
    ultimate_haste: float
    summoner_haste: float
    basic_haste: float = 0.0
    abilities: dict[str, AbilityCooldownResponseSchema]
    summoner_spells: list[SummonerCooldownResponseSchema]
