from aiogram import Bot, Dispatcher

from rtsu_students_bot.config import settings

bot = Bot(settings.bot.token, parse_mode="html")
dp = Dispatcher(bot)
