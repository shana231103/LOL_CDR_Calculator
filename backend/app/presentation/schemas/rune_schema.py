# File: backend/app/presentation/schemas/rune_schema.py

from pydantic import BaseModel


class RuneResponseSchema(BaseModel):
    id: int
    key: str
    name: str
    icon_url: str = ""
    haste_type: str
    base_haste: float = 0.0
    haste_per_stack: float = 0.0
    max_stacks: int = 0
