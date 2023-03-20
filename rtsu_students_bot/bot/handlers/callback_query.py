from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.bot.filters import AuthorizationFilter
from rtsu_students_bot.rtsu import RTSUApi
from rtsu_students_bot.template_engine import render_template
from rtsu_students_bot.models import User
from rtsu_students_bot.bot.keyboards import callbacks, inline
from rtsu_students_bot.bot.states import AuthState

from .core import start_auth, authorize_user


async def auth_callback_processor(
        query: types.CallbackQuery,
        user: User
):
    """
    Handles `callbacks.AUTH_CALLBACK`
    :param query: A callback-query
    :param user: An User
    """

    await start_auth(query, user)


async def cancel_callback_processor(
        query: types.CallbackQuery,
        state: FSMContext
):
    """
    Handles `callbacks.CANCELLATION_CALLBACK`
    :param state: A current state (fsm-context)
    :param query:
    :return:
    """

    await query.message.delete()

    await query.bot.send_message(
        query.from_user.id,
        text=render_template("cancellation.html")
    )
    await state.finish()


async def credentials_confirmation_callback_processor(
        query: types.CallbackQuery,
        callback_data: dict,
        db_session: AsyncSession,
        user: User,
        rtsu: RTSUApi,
        state: FSMContext
):
    """
    Processes `callbacks.CONFIRMATION_CALLBACK`
    :param state: A current state (fsm-context)
    :param rtsu: An initialized rtsu-api client
    :param user: A user in database
    :param db_session: `AsyncSession` object
    :param query: A callback-query
    :param callback_data: Callback's data
    """

    # If user clicks `Yes` - `1` will be passed
    # If user clicks `No` - `0` will be passed
    # So, all data will be represented as strings in telegram-callbacks
    # For getting boolean some converting needed
    # Firstly, we convert string to int, after, we convert this int to boolean
    ok = bool(int(callback_data.get("ok")))

    await query.answer()
    await query.message.delete()

    async with state.proxy() as data:
        login = data.get("login")
        password = data.get("password")

    if ok:
        await authorize_user(query, user, login, password, db_session, rtsu, state)
    else:
        await query.bot.send_message(
            query.from_user.id,
            text=render_template("auth.html", user=user),
            reply_markup=inline.cancellation_keyboard_factory()
        )
        await AuthState.first()


async def show_subject_processor(
        query: types.CallbackQuery,
        rtsu: RTSUApi,
        callback_data: dict,
):
    """
    Handles `callbacks.SUBJECT_CALLBACK`
    :param callback_data: A callback-data
    :param query: A query
    :param rtsu: Initialized RTSU API client
    """

    await query.answer()

    needed_subject_id = int(callback_data.get("id"))

    year = await rtsu.get_current_year_id()

    subjects = await rtsu.get_academic_year_subjects(year)

    needed_subject = list(filter(lambda x: x.id == needed_subject_id, subjects))

    if not needed_subject:
        await query.bot.send_message(
            query.from_user.id,
            "Дисциплина не найдена."
        )
        return

    await query.bot.send_message(
        query.from_user.id,
        text=render_template(
            "subject.html",
            subject=needed_subject[0]
        )
    )


async def delete_message_callback_processor(query: types.CallbackQuery):
    """
    Processes deletion-callback
    :param query: A callback-query
    :return:
    """
    await query.answer()
    await query.message.delete()


def setup(dp: Dispatcher):
    """
    Registers callback-query handlers
    :param dp: A `Dispatcher` instance
    """
    dp.register_callback_query_handler(
        auth_callback_processor, callbacks.AUTH_CALLBACK.filter(), AuthorizationFilter(False)
    )
    dp.register_callback_query_handler(cancel_callback_processor, callbacks.CANCELLATION_CALLBACK.filter())
    dp.register_callback_query_handler(
        credentials_confirmation_callback_processor, callbacks.CONFIRMATION_CALLBACK.filter(), state=AuthState.confirm
    )
    dp.register_callback_query_handler(
        show_subject_processor, callbacks.SUBJECT_CALLBACK.filter(), AuthorizationFilter(True)
    )
    dp.register_callback_query_handler(
        delete_message_callback_processor, callbacks.DELETE_MSG_CALLBACK.filter()
    )
