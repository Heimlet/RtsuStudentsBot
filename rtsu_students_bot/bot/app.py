from aiogram import Bot, Dispatcher

from rtsu_students_bot.config import settings

from .handlers import setup
from .dispatcher import bot, dp


def get_app() -> Dispatcher:
    """
    Initializes & returns `Dispatcher`
    """

    # Setup handlers

    setup(dp)

    return dp
