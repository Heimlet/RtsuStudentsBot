import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.service import user
from rtsu_students_bot.rtsu import RTSUApi


class UserMiddleware(BaseMiddleware):
    """
    Middleware for providing a `User` object
    """

    def __init__(self):
        """
        Initializes self
        """

        self._logger = logging.getLogger("users_middleware")
        super().__init__()

    async def _provide_user(self, user_id: int, data: dict) -> dict:
        """
        Fetches and returns user
        """

        if 'db_session' not in data:
            raise RuntimeError("AsyncSession not found.")

        if 'rtsu' not in data:
            raise RuntimeError("RTSU API client not found.")

        db_session: AsyncSession = data.get("db_session")
        rtsu_client: RTSUApi = data.get("rtsu")

        self._logger.debug(f"Getting user with ID {user_id}")

        u = await user.get_user_by_tg_id(db_session, user_id)

        if u is None:
            self._logger.debug(f"User with ID {user_id} not found, creating...")
            u = await user.create_user(db_session, telegram_id=user_id)

        self._logger.debug(f"User provided, {u}")

        # If user is authorized, lets setup `RTSU` client
        if u.is_authorized:
            rtsu_client.set_token(u.token)
            self._logger.debug("User is authorized, API-client's token initialized.")

        data["user"] = u

        return data

    async def on_pre_process_message(self, message: types.message, data: dict):
        """
        Method for preprocessing messages (provides user)
        :param message: A message
        :param data: A data from another middleware
        :return: None
        """

        return await self._provide_user(message.from_user.id, data)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        """
        Method for preprocessing callback-queries (provides user)
        :param data:
        :param query:
        :return:
        """

        return await self._provide_user(query.from_user.id, data)
