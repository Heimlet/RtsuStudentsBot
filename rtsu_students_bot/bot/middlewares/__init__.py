from aiogram import Dispatcher

from .resources_middleware import ResourcesMiddleware
from .user_middleware import UserMiddleware


def setup(dp: Dispatcher):
    """

    :param dp:
    :return:
    """

    dp.setup_middleware(ResourcesMiddleware())
    dp.setup_middleware(UserMiddleware())
