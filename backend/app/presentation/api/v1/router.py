# File: backend/app/presentation/api/v1/router.py

from fastapi import APIRouter
from app.presentation.api.v1.calculate import router as calculate_router
from app.presentation.api.v1.champions import router as champions_router
from app.presentation.api.v1.items import router as items_router
from app.presentation.api.v1.runes import router as runes_router
from app.presentation.api.v1.spells import router as spells_router
from app.presentation.api.v1.sync import router as sync_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(calculate_router)
api_v1_router.include_router(champions_router)
api_v1_router.include_router(items_router)
api_v1_router.include_router(runes_router)
api_v1_router.include_router(spells_router)
api_v1_router.include_router(sync_router)
