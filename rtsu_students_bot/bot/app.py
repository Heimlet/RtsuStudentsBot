from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from rtsu_students_bot.config import settings

from . import handlers, middlewares


def get_app() -> Dispatcher:
    """
    Initializes & returns `Dispatcher`
    """

    # Create bot & dispatcher

    memory_storage = MemoryStorage()

    bot = Bot(settings.bot.token, parse_mode="html")
    dp = Dispatcher(bot, storage=memory_storage)

    # Setup handlers

    handlers.setup(dp)

    # Setup middlewares

    middlewares.setup(dp)

    return dp
