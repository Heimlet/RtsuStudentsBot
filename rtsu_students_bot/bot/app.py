from aiogram import Bot, Dispatcher

from rtsu_students_bot.config import settings


def get_app() -> Dispatcher:
    """
    Initializes & returns `Dispatcher`
    """

    bot = Bot(settings.bot.token)
    dp = Dispatcher(bot)

    # TODO(Ilyas): Setup handlers

    return dp
