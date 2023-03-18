from aiogram import Bot, Dispatcher

from rtsu_students_bot.config import settings

from . import handlers, middlewares
from .dispatcher import bot, dp


def get_app() -> Dispatcher:
    """
    Initializes & returns `Dispatcher`
    """

    # Setup handlers

    handlers.setup(dp)
    middlewares.setup(dp)

    return dp
