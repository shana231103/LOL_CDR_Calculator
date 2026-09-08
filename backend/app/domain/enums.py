# File: backend/app/domain/enums.py

from enum import Enum


class SkillSlot(str, Enum):
    Q = "Q"
    W = "W"
    E = "E"
    R = "R"


class HasteType(str, Enum):
    ABILITY_HASTE = "ABILITY_HASTE"
    ULTIMATE_HASTE = "ULTIMATE_HASTE"
    BASIC_HASTE = "BASIC_HASTE"
    SUMMONER_HASTE = "SUMMONER_HASTE"


class SpellSlot(str, Enum):
    D = "D"
    F = "F"
