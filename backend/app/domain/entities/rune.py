# File: backend/app/domain/entities/rune.py

from dataclasses import dataclass
from app.domain.enums import HasteType
from app.domain.value_objects import AbilityHaste
from app.domain.exceptions import DomainError


@dataclass
class Rune:
    id: int
    key: str
    name: str
    icon_url: str
    haste_type: HasteType
    base_haste: float = 0.0
    haste_per_stack: float = 0.0
    max_stacks: int = 0

    def compute_total_haste(self, stacks: int = 0) -> float:
        bounded_stacks = max(0, min(stacks, self.max_stacks))
        return self.base_haste + (self.haste_per_stack * bounded_stacks)


@dataclass
class RuneSelection:
    rune: Rune
    stacks: int = 0

    def __post_init__(self) -> None:
        if self.stacks < 0:
            raise DomainError(f"Rune stacks cannot be negative: {self.stacks}")
        if self.rune.max_stacks > 0 and self.stacks > self.rune.max_stacks:
            raise DomainError(
                f"Stacks {self.stacks} exceeds max stacks {self.rune.max_stacks} for rune {self.rune.name}."
            )

    def calculate_haste(self) -> tuple[HasteType, AbilityHaste]:
        val = self.rune.compute_total_haste(self.stacks)
        return self.rune.haste_type, AbilityHaste(val)
