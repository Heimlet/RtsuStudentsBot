from aiogram import types, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.rtsu import RTSUApi
from rtsu_students_bot.bot.filters import AuthorizationFilter
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


async def help_cmd(message: types.Message):
    """
    Handles `help` cmd
    :param message: A message
    """

    await core.show_help(message)


async def statistics(message: types.Message, rtsu: RTSUApi):
    """
    Handles `statistics` cmd
    :param message: A message
    :param rtsu: Initialized RTSU API client
    """

    await core.show_statistics(message, rtsu)


async def subjects(message: types.Message, rtsu: RTSUApi):
    """
    Handles `subjects` cmd
    :param message: A message
    :param rtsu: Initialized RTSU API client
    """

    await core.show_subjects(message, rtsu)


async def profile(message: types.Message, rtsu: RTSUApi, user: User):
    """
    Handles `profile` cmd
    :param message: A message
    :param user: User in db
    :param rtsu: Initialized RTSU API client
    """

    await core.show_profile(message, rtsu, user)


async def logout(message: types.Message, user: User, db_session: AsyncSession):
    """
    Handles `logout` cmd
    :param db_session: `AsyncSession` object
    :param user: A user in db
    :param message: A message
    """

    await core.logout_user(message, user, db_session)


async def about(message: types.Message):
    """
    Handles `about` cmd
    :param message: A message
    """

    await core.show_about(message)


def setup(dp: Dispatcher):
    """
    Setups commands-handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help_cmd, commands=["help"])
    dp.register_message_handler(about, commands=["about"])
    dp.register_message_handler(logout, AuthorizationFilter(True), commands=["logout"])
    dp.register_message_handler(profile, AuthorizationFilter(True), commands=["profile"])
    dp.register_message_handler(subjects, AuthorizationFilter(True), commands=["subjects"])
    dp.register_message_handler(statistics, AuthorizationFilter(True), commands=["stat"])
    dp.register_message_handler(auth, AuthorizationFilter(False), commands=["auth"])
    dp.register_message_handler(auth, AuthorizationFilter(authorized=True), commands=["auth"])
