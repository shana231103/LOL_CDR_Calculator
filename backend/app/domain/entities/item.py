# File: backend/app/domain/entities/item.py

from dataclasses import dataclass
from app.domain.value_objects import AbilityHaste


@dataclass
class Item:
    id: int
    name: str
    description: str
    image_url: str
    ability_haste: float = 0.0
    ultimate_haste: float = 0.0
    basic_haste: float = 0.0
    summoner_haste: float = 0.0
    gold_total: int = 0
    locale: str = "vi_VN"

    def get_haste(self) -> AbilityHaste:
        return AbilityHaste(max(0.0, float(self.ability_haste)))
