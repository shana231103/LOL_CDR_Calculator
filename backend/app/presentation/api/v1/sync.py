# File: backend/app/presentation/api/v1/sync.py

from typing import Any
from fastapi import APIRouter, Depends, Query
from app.infrastructure.di.container import get_sync_patch_use_case
from app.application.use_cases.sync_patch_data import SyncPatchDataUseCase

router = APIRouter(prefix="/sync", tags=["Synchronization"])


@router.post("", response_model=dict[str, Any])
async def trigger_patch_sync(
    force: bool = Query(default=False, description="Force re-sync even if active patch matches"),
    locales: str | None = Query(default="vi_VN,en_US", description="Comma-separated locales, e.g. vi_VN,en_US"),
    use_case: SyncPatchDataUseCase = Depends(get_sync_patch_use_case),
) -> dict[str, Any]:
    target_locales = [loc.strip() for loc in locales.split(",") if loc.strip()] if locales else ["vi_VN", "en_US"]
    return await use_case.execute(force=force, locales=target_locales)
