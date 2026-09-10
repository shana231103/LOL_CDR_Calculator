# File: backend/app/application/use_cases/get_runes.py

from app.domain.repositories.rune_repository import IRuneRepository
from app.application.dtos.rune_dto import RuneDTO


class GetRunesUseCase:
    def __init__(self, rune_repo: IRuneRepository) -> None:
        self._rune_repo = rune_repo

    async def execute(self, locale: str = "vi_VN") -> list[RuneDTO]:
        runes = await self._rune_repo.get_haste_runes(locale=locale)
        return [
            RuneDTO(
                id=rune.id,
                key=rune.key,
                name=rune.name,
                icon_url=rune.icon_url,
                haste_type=rune.haste_type.value,
                base_haste=rune.base_haste,
                haste_per_stack=rune.haste_per_stack,
                max_stacks=rune.max_stacks,
            )
            for rune in runes
        ]
