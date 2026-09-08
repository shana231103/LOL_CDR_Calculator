# File: backend/app/presentation/schemas/item_schema.py

from pydantic import BaseModel


class ItemResponseSchema(BaseModel):
    id: int
    name: str
    description: str = ""
    image_url: str = ""
    ability_haste: float = 0.0
    ultimate_haste: float = 0.0
    basic_haste: float = 0.0
    summoner_haste: float = 0.0
    gold_total: int = 0
