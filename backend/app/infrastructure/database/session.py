# File: backend/app/infrastructure/database/session.py

from collections.abc import AsyncGenerator
from functools import lru_cache
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.models.base import Base


@lru_cache
def get_async_engine() -> AsyncEngine:
    settings = get_settings()
    url = settings.database_url
    connect_args = {}
    if "sqlite" in url:
        connect_args["check_same_thread"] = False
    return create_async_engine(
        url,
        echo=settings.debug,
        future=True,
        connect_args=connect_args,
    )


@lru_cache
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Initializes schema tables and upgrades legacy schemas if needed."""
    engine = get_async_engine()
    async with engine.begin() as conn:
        def check_and_create(sync_conn):
            inspector = inspect(sync_conn)
            tables = inspector.get_table_names()
            if "champions" in tables:
                columns = [c["name"] for c in inspector.get_columns("champions")]
                if "locale" not in columns:
                    Base.metadata.drop_all(sync_conn)
            Base.metadata.create_all(sync_conn)

        await conn.run_sync(check_and_create)
