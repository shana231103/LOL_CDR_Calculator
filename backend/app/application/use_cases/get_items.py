# File: backend/app/application/use_cases/get_items.py

from app.domain.repositories.item_repository import IItemRepository
from app.application.dtos.item_dto import ItemDTO


class GetItemsUseCase:
    def __init__(self, item_repo: IItemRepository) -> None:
        self._item_repo = item_repo

    async def execute(self, search: str | None = None) -> list[ItemDTO]:
        items = await self._item_repo.get_all(search)
        return [
            ItemDTO(
                id=item.id,
                name=item.name,
                description=item.description,
                image_url=item.image_url,
                ability_haste=item.ability_haste,
                gold_total=item.gold_total,
                ultimate_haste=item.ultimate_haste,
                basic_haste=item.basic_haste,
                summoner_haste=item.summoner_haste,
            )
            for item in items
        ]
