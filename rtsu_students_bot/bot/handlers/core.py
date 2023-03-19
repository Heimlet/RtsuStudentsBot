"""
`core.py` - Core-functionality of bot
"""

from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.service import user
from rtsu_students_bot.rtsu import RTSUApi, exceptions
from rtsu_students_bot.bot.keyboards import inline, reply
from rtsu_students_bot.bot.states import AuthState
from rtsu_students_bot.models import User
from rtsu_students_bot.template_engine import render_template


async def start_auth(
        update: Union[types.CallbackQuery, types.Message],
        user_in_db: User
):
    """
    Core-function, starts authentification process
    :param update: An `update` (message or query)
    :param user_in_db: An User in database
    :return:
    """

    markup = None
    text = render_template(
        "auth.html",
        user=user_in_db
    )

    if not user_in_db.is_authorized:
        await AuthState.first()
        markup = inline.cancellation_keyboard_factory()

    await update.bot.send_message(
        update.from_user.id,
        text=text,
        reply_markup=markup
    )


async def authorize_user(
        update: Union[types.CallbackQuery, types.Message],
        user_in_db: User,
        login: str,
        password: str,
        db_session: AsyncSession,
        rtsu_client: RTSUApi,
        state: FSMContext
):
    """
    Authorizes user, on success auth, saves token to database
    :param state: A state (fsm-context)
    :param rtsu_client: An initialized RTSU api client
    :param db_session: `AsyncSession` object
    :param password: A password
    :param login: A login
    :param user_in_db: A user in database
    :param update: Update (message or query)
    """

    try:
        auth_schema = await rtsu_client.auth(login, password)
    except exceptions.AuthError:
        await update.bot.send_message(
            update.from_user.id,
            text=render_template("auth_error.html"),
            reply_markup=inline.cancellation_keyboard_factory()
        )
        await AuthState.first()
        return

    profile = await rtsu_client.get_profile()

    await user.update_user(
        db_session,
        user_in_db.id,
        full_name=profile.full_name.ru,
    )

    await user.update_user_token(
        db_session,
        update.from_user.id,
        auth_schema.token,
    )

    await update.bot.send_message(
        update.from_user.id,
        text=render_template("auth_success.html", full_name=profile.full_name.ru),
        reply_markup=reply.main_menu_factory()
    )
    await state.finish()
