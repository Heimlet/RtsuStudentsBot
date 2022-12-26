from aiogram import Bot, Dispatcher
from aiogram.utils import executor


def start(webhooks: bool = False):
    """Starts the bot"""

    bot = Bot()
