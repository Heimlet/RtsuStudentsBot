from aiogram import Dispatcher

from . import commands, callback_query


def setup(dp: Dispatcher):
    """

    :param dp:
    :return:
    """

    commands.setup(dp)
