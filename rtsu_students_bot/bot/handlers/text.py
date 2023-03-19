"""
`text.py` - Text handlers
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from rtsu_students_bot.bot.states import AuthState
from rtsu_students_bot.template_engine import render_template
from rtsu_students_bot.bot.keyboards import inline


async def login_handler(
        message: types.Message,
        state: FSMContext
):
    """
    Handles `login` of user
    :param message: A message with login
    :param state: A current state (fsm-context)
    """

    async with state.proxy() as data:
        data["login"] = message.text

    await AuthState.next()
    await message.delete()

    await message.bot.send_message(
        message.from_user.id,
        render_template("enter_password.html"),
        reply_markup=inline.cancellation_keyboard_factory()
    )


async def password_handler(
        message: types.Message,
        state: FSMContext,
):
    """
    Handles password of user
    :param message: A message (with password)
    :param state: A state (fsm-context)
    """

    async with state.proxy() as data:
        password = data["password"] = message.text
        login = data["login"]

    await AuthState.next()
    await message.delete()

    await message.bot.send_message(
        message.from_user.id,
        render_template("credentials_confirmation.html", login=login, password=password),
        reply_markup=inline.confirmation_keyboard_factory()
    )


def setup(dp: Dispatcher):
    """
    Setups text-handlers
    :param dp: A `Dispatcher` instance
    """
    dp.register_message_handler(login_handler, state=AuthState.login, content_types=[types.ContentType.TEXT])
    dp.register_message_handler(password_handler, state=AuthState.password, content_types=[types.ContentType.TEXT])
