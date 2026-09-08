# File: backend/app/application/dtos/item_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ItemDTO:
    id: int
    name: str
    description: str
    image_url: str
    ability_haste: float
    gold_total: int
    ultimate_haste: float = 0.0
    basic_haste: float = 0.0
    summoner_haste: float = 0.0
