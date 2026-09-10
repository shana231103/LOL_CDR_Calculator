# File: backend/app/domain/entities/spell.py

from dataclasses import dataclass
from app.domain.value_objects import Cooldown


@dataclass
class SummonerSpell:
    id: str
    key: str
    name: str
    description: str
    cooldown: float
    image_url: str
    locale: str = "vi_VN"

    def get_base_cooldown(self) -> Cooldown:
        return Cooldown(max(0.0, float(self.cooldown)))
