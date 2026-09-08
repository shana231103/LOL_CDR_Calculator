# File: backend/app/application/dtos/spell_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class SpellDTO:
    id: str
    key: str
    name: str
    description: str
    cooldown: float
    image_url: str
