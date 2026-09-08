# File: backend/app/presentation/schemas/champion_schema.py

from pydantic import BaseModel, Field


class AbilityResponseSchema(BaseModel):
    id: str
    slot: str
    name: str
    description: str = ""
    image_url: str = ""
    max_rank: int = 5
    cooldowns: list[float] = Field(default_factory=list)


class ChampionResponseSchema(BaseModel):
    id: str
    key: str
    name: str
    title: str
    image_url: str
    abilities: list[AbilityResponseSchema] = Field(default_factory=list)
