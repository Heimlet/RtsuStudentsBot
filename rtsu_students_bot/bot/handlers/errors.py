import logging

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import InvalidQueryID, MessageNotModified

from rtsu_students_bot.rtsu.exceptions import ServerError
from rtsu_students_bot.template_engine import render_template


async def invalid_query_error_handler(update, error):
    """
    Handles `InvalidQueryError`
    :param update:
    :param error:
    :return:
    """
    logging.info(f"OK, Invalid query ID, {error}, {update}")
    return True


async def message_not_modified_error_handler(update, error):
    """
    Handles `MessageNotModifiedError`
    :param update:
    :param error:
    :return:
    """
    logging.info(f"OK, Message not modified, {error}, {update}")
    return True


async def server_error_handler(update: types.Update, error: ServerError):
    """
    Handles `ServerError`
    :param update:
    :param error:
    :return:
    """

    logging.exception("Server error", exc_info=error)

    if update.message:
        chat_id = update.message.from_user.id
    else:
        chat_id = update.callback_query.from_user.id

    await update.bot.send_message(
        chat_id=chat_id,
        text=render_template("server_error.html")
    )

    return True


async def any_exception_handler(update: types.Update, error: Exception):
    """
    Handles `Exception`
    :param update:
    :param error:
    :return:
    """
    logging.error(f"{error.__class__.__name__} has been thrown")
    logging.exception("Exception", exc_info=error)
    return True


def setup(dp: Dispatcher):
    """
    Registers error handlers
    :param dp: A `Dispatcher` instance
    """
    dp.register_errors_handler(
        server_error_handler,
        exception=ServerError
    )
    dp.register_errors_handler(
        invalid_query_error_handler,
        exception=InvalidQueryID
    )
    dp.register_errors_handler(
        message_not_modified_error_handler,
        exception=MessageNotModified
    )
    dp.register_errors_handler(
        any_exception_handler,
        exception=Exception
    )
