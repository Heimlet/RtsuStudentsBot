from aiogram import Bot, Dispatcher

from rtsu_students_bot.config import settings


def dispatcher_factory() -> Dispatcher:
    """
    Builds & returns `Bot` with `Dispatcher`
    """

    bot = Bot(settings.bot.token)
    dp = Dispatcher(bot)

    # TODO(Ilyas): Setup handlers

    return dp
