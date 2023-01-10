from fastapi import FastAPI

from ..config import Settings
from .routers import users_router


def app_factory(settings: Settings):
    """Builds & returns application."""
    built_app = FastAPI()

    built_app.include_router(users_router)
