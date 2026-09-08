# File: backend/app/infrastructure/repositories/sql_patch_repo.py

from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repositories.patch_repository import IPatchRepository
from app.infrastructure.database.models.patch_orm import PatchORM


class SqlPatchRepository(IPatchRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_active_patch(self) -> str | None:
        stmt = select(PatchORM).where(PatchORM.id == 1)
        res = await self._session.execute(stmt)
        record = res.scalar_one_or_none()
        return record.version if record else None

    async def set_active_patch(self, patch_version: str) -> None:
        record = await self._session.get(PatchORM, 1)
        if record:
            record.version = patch_version
            record.updated_at = datetime.now(timezone.utc)
        else:
            self._session.add(
                PatchORM(
                    id=1,
                    version=patch_version,
                    updated_at=datetime.now(timezone.utc),
                )
            )
        await self._session.flush()
