from fastapi import FastAPI

from ..settings import Settings


def app_factory(settings: Settings):
    """Builds & returns application."""
    built_app = FastAPI()
