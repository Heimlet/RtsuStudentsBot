import logging

from aiogram import types, Dispatcher, Bot

from rtsu_students_bot.config import settings

BOT_COMMANDS = [
    types.BotCommand(
        "start",
        "Запуск бота"
    ),
]


def configure_logging():
    """
    Configures logging
    """

    level = logging.INFO

    if settings.logging.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, format=settings.logging.format)


async def setup_commands(bot: Bot):
    """
    Configures bot-commands
    """

    logging.info("Setting up commands.")

    await bot.set_my_commands(
        BOT_COMMANDS
    )


async def startup_handler(dp: Dispatcher):
    """
    Startup handler
    :param dp: A `Dispatcher` instance
    """

    configure_logging()

    await setup_commands(dp.bot)

    logging.info("Starting bot.")
