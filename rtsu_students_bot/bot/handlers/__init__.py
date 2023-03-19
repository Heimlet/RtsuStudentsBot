from aiogram import Dispatcher

from . import (
    commands, callback_query, startup,
    text,
)


def setup(dp: Dispatcher):
    """

    :param dp:
    :return:
    """

    commands.setup(dp)
    callback_query.setup(dp)
    text.setup(dp)
