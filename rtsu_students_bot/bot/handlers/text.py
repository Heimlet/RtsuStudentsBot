"""
`text.py` - Text handlers
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.bot.filters import AuthorizationFilter
from rtsu_students_bot.rtsu import RTSUApi
from rtsu_students_bot.models import User
from rtsu_students_bot.bot.states import AuthState
from rtsu_students_bot.template_engine import render_template
from rtsu_students_bot.bot.keyboards import inline

from . import core


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


async def show_profile_handler(
        message: types.Message,
        rtsu: RTSUApi,
        user: User,
):
    """
    Handles 'Show profile' request
    :param message: A message
    :param rtsu: Initialized RTSU API client
    :param user: A user from db
    :return:
    """

    await core.show_profile(message, rtsu, user)


async def show_statistics_handler(
        message: types.Message,
        rtsu: RTSUApi,
):
    """
    Shows user's statistics
    :param message:
    :param rtsu:
    :return:
    """

    await core.show_statistics(message, rtsu)


async def show_subjects_handler(
        message: types.Message,
        rtsu: RTSUApi
):
    """
    Handles 'Show statistics' request
    :param rtsu: Initialized RTSU API client
    :param message: A message
    :return:
    """

    await core.show_subjects(message, rtsu)


async def logout_handler(
        message: types.Message,
        user: User,
        db_session: AsyncSession,
):
    """
    Handles 'logout-request'
    :param db_session: `AsyncSession` object
    :param message: A message
    :param user: A user in db
    """

    await core.logout_user(message, user, db_session)


async def auth_handler(message: types.Message, user: User):
    """
    Handles 'auth-request'
    :param message: A message
    :param user: A user in db
    :return:
    """

    await core.start_auth(message, user)


async def help_handler(message: types.Message):
    """
    Handles 'help-request'
    :param message: A message
    :return:
    """

    await core.show_help(message)


async def about_handler(message: types.Message):
    """
    Handles 'about-request'
    :param message: A message
    :return:
    """

    await core.show_about(message)


def setup(dp: Dispatcher):
    """
    Setups text-handlers
    :param dp: A `Dispatcher` instance
    """
    dp.register_message_handler(
        login_handler,
        state=AuthState.login,
        content_types=[types.ContentType.TEXT],
    )
    dp.register_message_handler(password_handler, state=AuthState.password, content_types=[types.ContentType.TEXT])
    dp.register_message_handler(
        show_profile_handler, Text(equals="🎓 Профиль"), AuthorizationFilter(authorized=True)
    )
    dp.register_message_handler(
        show_statistics_handler, Text(equals="📊 Статистика"), AuthorizationFilter(authorized=True)
    )
    dp.register_message_handler(
        show_subjects_handler, Text(equals="📕 Дисциплины"), AuthorizationFilter(authorized=True)
    )
    dp.register_message_handler(
        logout_handler, Text(equals="◀️ Выход из системы"), AuthorizationFilter(authorized=True)
    )
    dp.register_message_handler(
        auth_handler, Text(equals="🔑 Авторизация"), AuthorizationFilter(authorized=False)
    )
    dp.register_message_handler(
        help_handler, Text(equals="🆘 Инструкция"),
    )

    dp.register_message_handler(
        about_handler, Text(equals="ℹ️ О боте"),
    )
