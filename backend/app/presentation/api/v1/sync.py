# File: backend/app/presentation/api/v1/sync.py

from typing import Any
from fastapi import APIRouter, Depends, Query
from app.infrastructure.di.container import get_sync_patch_use_case
from app.application.use_cases.sync_patch_data import SyncPatchDataUseCase

router = APIRouter(prefix="/sync", tags=["Synchronization"])


@router.post("", response_model=dict[str, Any])
async def trigger_patch_sync(
    force: bool = Query(default=False, description="Force re-sync even if active patch matches"),
    use_case: SyncPatchDataUseCase = Depends(get_sync_patch_use_case),
) -> dict[str, Any]:
    return await use_case.execute(force=force)
