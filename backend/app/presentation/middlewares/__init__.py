# File: backend/app/presentation/middlewares/__init__.py

from app.presentation.middlewares.error_handler import setup_exception_handlers

__all__ = ["setup_exception_handlers"]
