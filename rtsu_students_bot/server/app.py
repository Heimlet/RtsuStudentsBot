from fastapi import FastAPI, APIRouter

from ..config import Settings
from .routers import users_router

router = APIRouter()


def app_factory(settings: Settings):
    """Builds & returns application."""
    built_app = FastAPI(
        description="API for RTSU.Students bot.",
        title="RTSU.Students bot API",
        version="1.0"
    )

    built_app.include_router(users_router)
