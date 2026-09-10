# File: backend/app/domain/entities/champion.py

from dataclasses import dataclass, field
from app.domain.enums import SkillSlot
from app.domain.entities.ability import Ability
from app.domain.exceptions import EntityNotFoundError


@dataclass
class Champion:
    id: str
    key: str
    name: str
    title: str
    image_url: str
    locale: str = "vi_VN"
    abilities: dict[SkillSlot, Ability] = field(default_factory=dict)

    def get_ability(self, slot: SkillSlot) -> Ability:
        if slot not in self.abilities:
            raise EntityNotFoundError(
                f"Ability for slot {slot.value} not found on champion {self.name}."
            )
        return self.abilities[slot]

    def add_ability(self, ability: Ability) -> None:
        self.abilities[ability.slot] = ability
