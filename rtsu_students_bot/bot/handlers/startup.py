import logging

from aiogram import types, Dispatcher

BOT_COMMANDS = [
    types.BotCommand(
        "start",
        "Запуск бота"
    ),
]


async def startup_handler(dp: Dispatcher):
    """
    Startup handler
    :return:
    """

    logger = logging.getLogger("bot")

    logger.info("Setting up commands.")

    await dp.bot.set_my_commands(
        BOT_COMMANDS
    )

    logging.info("Starting bot.")
