import logging
from typing import Optional

import cashews

from aiogram import types, Dispatcher, Bot

from rtsu_students_bot.config import settings
from rtsu_students_bot.database import engine
from rtsu_students_bot.models import Base

BOT_COMMANDS = [
    types.BotCommand(
        "start",
        "Запуск бота"
    ),
    types.BotCommand(
        "auth",
        "Авторизация в системе"
    ),
    types.BotCommand(
        "profile",
        "Профиль РТСУ"
    ),
    types.BotCommand(
        "stat",
        "Общая статистика"
    ),
    types.BotCommand(
        "subjects",
        "Дисциплины"
    ),
    types.BotCommand(
        "help",
        "Помощь"
    ),
    types.BotCommand(
        "about",
        "О боте"
    ),
    types.BotCommand(
        "logout",
        "Выход из системы"
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


def setup_cache():
    """
    Configures cache
    """
    logging.info("Setting up cache...")
    cashews.setup("mem://")


async def setup_db():
    """
    Initializes db (creates tables, etc...)
    :return:
    """
    logging.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def setup_commands(bot: Bot):
    """
    Configures bot-commands
    """

    logging.info("Setting up commands.")

    await bot.set_my_commands(
        BOT_COMMANDS
    )


async def configure_webhooks(url: str, dp: Dispatcher):
    """
    Configures webhooks
    :param url: Url
    :param dp: Dispatcher
    :return:
    """
    logging.info(f"Settings webhooks [{url}]")
    await dp.bot.set_webhook(url)


def startup_handler_factory(webhook_url: Optional[str] = None) -> callable:
    async def inner_func(dp: Dispatcher):
        """
        Startup handler
        :param dp: A `Dispatcher` instance
        """

        configure_logging()

        if webhook_url:
            await configure_webhooks(webhook_url, dp)

        setup_cache()
        await setup_db()
        await setup_commands(dp.bot)

        logging.info("Starting bot.")

    return inner_func
