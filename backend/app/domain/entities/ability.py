# File: backend/app/domain/entities/ability.py

from dataclasses import dataclass
from app.domain.enums import SkillSlot
from app.domain.value_objects import Cooldown
from app.domain.exceptions import InvalidRankError


@dataclass
class Ability:
    id: str
    slot: SkillSlot
    name: str
    description: str
    image_url: str
    max_rank: int
    cooldowns: list[float]

    def get_cooldown_for_rank(self, rank: int) -> Cooldown:
        if not (1 <= rank <= self.max_rank):
            raise InvalidRankError(
                f"Rank {rank} is outside allowable range [1, {self.max_rank}] for ability {self.name}."
            )
        
        # If cooldowns array has fewer entries than max_rank, fallback to last or 0.0
        index = rank - 1
        if 0 <= index < len(self.cooldowns):
            return Cooldown(self.cooldowns[index])
        elif self.cooldowns:
            return Cooldown(self.cooldowns[-1])
        return Cooldown(0.0)
