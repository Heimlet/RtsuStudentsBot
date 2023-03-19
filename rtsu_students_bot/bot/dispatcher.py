from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from rtsu_students_bot.config import settings

bot = Bot(settings.bot.token, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())
