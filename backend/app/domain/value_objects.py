# File: backend/app/domain/value_objects.py

from dataclasses import dataclass
from app.domain.exceptions import InvalidRankError, InvalidHasteError


@dataclass(frozen=True)
class Cooldown:
    seconds: float

    def __post_init__(self) -> None:
        if self.seconds < 0:
            raise InvalidHasteError(f"Cooldown cannot be negative: {self.seconds}")

    @property
    def rounded(self) -> float:
        return round(self.seconds, 2)


@dataclass(frozen=True)
class AbilityHaste:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise InvalidHasteError(f"Haste cannot be negative: {self.value}")

    def __add__(self, other: "AbilityHaste") -> "AbilityHaste":
        return AbilityHaste(self.value + other.value)


@dataclass(frozen=True)
class SkillRank:
    rank: int
    max_rank: int

    def __post_init__(self) -> None:
        if self.max_rank < 1:
            raise InvalidRankError(f"Max rank must be at least 1, got {self.max_rank}")
        if not (1 <= self.rank <= self.max_rank):
            raise InvalidRankError(
                f"Rank {self.rank} is outside allowable range [1, {self.max_rank}]."
            )


@dataclass(frozen=True)
class PatchVersion:
    version: str

    def __post_init__(self) -> None:
        if not self.version or not self.version.strip():
            raise ValueError("Patch version string cannot be empty.")
