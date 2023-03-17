from aiogram import types, Dispatcher

from rtsu_students_bot.bot.keyboards import inline
from rtsu_students_bot.template_engine import render_template


async def start(message: types.Message):
    """
    Handles `/start` cmd
    :param message: A message
    """

    await message.reply(
        text=render_template("start.html", user=message.from_user.full_name),
        reply_markup=inline.start_keyboard_factory()
    )


def setup(dp: Dispatcher):
    """
    Setups commands-handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=["start"])
