# File: backend/app/application/use_cases/get_spells.py

from app.domain.repositories.spell_repository import ISpellRepository
from app.application.dtos.spell_dto import SpellDTO


class GetSpellsUseCase:
    def __init__(self, spell_repo: ISpellRepository) -> None:
        self._spell_repo = spell_repo

    async def execute(self) -> list[SpellDTO]:
        spells = await self._spell_repo.get_all()
        return [
            SpellDTO(
                id=s.id,
                key=s.key,
                name=s.name,
                description=s.description,
                cooldown=s.cooldown,
                image_url=s.image_url,
            )
            for s in spells
        ]
