from typing import Union

from aiogram.dispatcher.filters import Filter
from aiogram.dispatcher.handler import ctx_data
from aiogram import types

from rtsu_students_bot.models import User
from rtsu_students_bot.template_engine import render_template


class AuthorizationFilter(Filter):
    """
    Filter for checking user's authorization
    """

    def __init__(self, authorized: bool):
        """
        Initializes self
        :param authorized:Is admin?
        """
        self.authorized = authorized

    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        """
        Checks for user's authorization status
        :param message: A message
        """

        data = ctx_data.get()

        user: User = data.get("user")

        if self.authorized is None:
            return True

        if self.authorized and not user.is_authorized:
            await message.bot.send_message(
                message.from_user.id,
                text=render_template("not_authorized.html")
            )
            return False
        elif not self.authorized and user.is_authorized:
            await message.bot.send_message(
                message.from_user.id,
                text=render_template("already_authorized.html")
            )
            return False

        return True
