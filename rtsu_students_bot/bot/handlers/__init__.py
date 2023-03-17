from aiogram import Dispatcher

from . import (
    commands, callback_query, startup
)


def setup(dp: Dispatcher):
    """

    :param dp:
    :return:
    """

    commands.setup(dp)
