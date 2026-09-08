# File: backend/app/presentation/middlewares/error_handler.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import (
    DomainError,
    InvalidRankError,
    InvalidHasteError,
    ItemLimitError,
    SpellLimitError,
    EntityNotFoundError,
)


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidRankError)
    async def invalid_rank_handler(request: Request, exc: InvalidRankError):
        return JSONResponse(
            status_code=400,
            content={"error": "INVALID_RANK", "detail": exc.message},
        )

    @app.exception_handler(ItemLimitError)
    async def item_limit_handler(request: Request, exc: ItemLimitError):
        return JSONResponse(
            status_code=400,
            content={"error": "ITEM_LIMIT", "detail": exc.message},
        )

    @app.exception_handler(SpellLimitError)
    async def spell_limit_handler(request: Request, exc: SpellLimitError):
        return JSONResponse(
            status_code=400,
            content={"error": "SPELL_LIMIT", "detail": exc.message},
        )

    @app.exception_handler(InvalidHasteError)
    async def invalid_haste_handler(request: Request, exc: InvalidHasteError):
        return JSONResponse(
            status_code=400,
            content={"error": "INVALID_HASTE", "detail": exc.message},
        )

    @app.exception_handler(EntityNotFoundError)
    async def not_found_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "NOT_FOUND", "detail": exc.message},
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        return JSONResponse(
            status_code=400,
            content={"error": "DOMAIN_ERROR", "detail": exc.message},
        )
