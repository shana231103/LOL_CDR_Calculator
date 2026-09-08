# File: backend/app/domain/exceptions.py


class DomainError(Exception):
    """Base exception for all domain errors."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvalidRankError(DomainError):
    """Raised when an ability rank is outside valid boundaries."""
    pass


class InvalidHasteError(DomainError):
    """Raised when haste or cooldown values are negative or mathematically invalid."""
    pass


class ItemLimitError(DomainError):
    """Raised when more than 6 items are assigned to a build."""
    pass


class SpellLimitError(DomainError):
    """Raised when more than 2 summoner spells are assigned to a build."""
    pass


class EntityNotFoundError(DomainError):
    """Raised when an entity is not found in the domain."""
    pass
