# File: backend/app/presentation/schemas/spell_schema.py

from pydantic import BaseModel


class SpellResponseSchema(BaseModel):
    id: str
    key: str
    name: str
    description: str = ""
    cooldown: float = 0.0
    image_url: str = ""
