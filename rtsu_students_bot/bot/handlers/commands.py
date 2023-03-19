from aiogram import types, Dispatcher

from rtsu_students_bot.models import User
from rtsu_students_bot.bot.keyboards import inline, reply
from rtsu_students_bot.template_engine import render_template

from . import core


async def start(message: types.Message, user: User):
    """
    Handles `/start` cmd
    :param user:
    :param message: A message
    """

    markup = reply.main_menu_factory()

    if not user.is_authorized:
        markup = inline.auth_keyboard_factory()

    await message.reply(
        text=render_template(
            "start.html",
            user=user,
            telegram_user=message.from_user
        ),
        reply_markup=markup,
    )


async def auth(message: types.Message, user: User):
    """
    Handles `/auth` cmd
    :param user: A User
    :param message: A message
    """

    await core.start_auth(message, user)


def setup(dp: Dispatcher):
    """
    Setups commands-handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(auth, commands=["auth"])
