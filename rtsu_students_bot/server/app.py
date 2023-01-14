import logging

from fastapi import FastAPI, APIRouter

from ..config import settings
from .routers import users_router
from .database import engine
from .models import Base

router = APIRouter()


async def startup_event_handler():
    # Firstly, configure logging
    level = logging.INFO
    logging.getLogger("uvicorn").handlers.clear()

    if settings.logging.debug:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format=settings.logging.format
    )
    logging.info("Logging configured.")

    # Configure database

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logging.info("Database configured.")


def app_factory() -> FastAPI:
    """Builds & returns application."""
    built_app = FastAPI(
        description="API for RTSU.Students bot.",
        title="RTSU.Students bot API",
        version="1.0"
    )

    built_app.add_event_handler("startup", startup_event_handler)

    built_app.include_router(users_router)

    return built_app


app = app_factory()
