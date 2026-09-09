# File: backend/app/presentation/api/v1/items.py

from fastapi import APIRouter, Depends, Query
from app.infrastructure.di.container import get_items_use_case
from app.application.use_cases.get_items import GetItemsUseCase
from app.presentation.schemas.item_schema import ItemResponseSchema

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=list[ItemResponseSchema])
async def list_items(
    search: str | None = Query(default=None, description="Search items by name"),
    use_case: GetItemsUseCase = Depends(get_items_use_case),
) -> list[ItemResponseSchema]:
    items = await use_case.execute(search)
    return [
        ItemResponseSchema(
            id=item.id,
            name=item.name,
            description=item.description,
            image_url=item.image_url,
            ability_haste=item.ability_haste,
            ultimate_haste=item.ultimate_haste,
            basic_haste=item.basic_haste,
            summoner_haste=item.summoner_haste,
            gold_total=item.gold_total,
        )
        for item in items
    ]
