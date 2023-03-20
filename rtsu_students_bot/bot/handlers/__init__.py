from aiogram import Dispatcher

from . import (
    commands, callback_query, startup,
    text, errors
)


def setup(dp: Dispatcher):
    """

    :param dp:
    :return:
    """

    commands.setup(dp)
    callback_query.setup(dp)
    text.setup(dp)
    errors.setup(dp)
