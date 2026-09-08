# File: backend/app/application/dtos/rune_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class RuneDTO:
    id: int
    key: str
    name: str
    icon_url: str
    haste_type: str
    base_haste: float
    haste_per_stack: float
    max_stacks: int
