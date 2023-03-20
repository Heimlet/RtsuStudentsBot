import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.rtsu import RTSUApi
from rtsu_students_bot.database import engine


class ResourcesMiddleware(BaseMiddleware):
    """
    Middleware for providing resources like db-connection and RTSU-client
    """

    def __init__(self):
        """
        Initializes self
        """

        self._logger = logging.getLogger("resources_middleware")

        super().__init__()

    @staticmethod
    async def _provide_api_client() -> RTSUApi:
        """
        Provides `RTSU` api client
        :return: Initialized client
        """

        client = RTSUApi()

        return client

    @staticmethod
    async def _provide_db_session() -> AsyncSession:
        """
        Provides `AsyncSession` object
        :return: Initialized session
        """

        session = AsyncSession(engine)

        return session

    async def _provide_resources(self) -> dict:
        """
        Initializes & provides needed resources, such as `RTSU-api-client` and `AsyncSession`
        :return:
        """
        self._logger.debug("Providing resources")
        api_client = await self._provide_api_client()
        db_session = await self._provide_db_session()

        resources = {
            "rtsu": api_client,
            "db_session": db_session,
        }

        return resources

    async def _cleanup(self, data: dict):
        """
        Closes connections & etc.
        :param data:
        :return:
        """

        self._logger.debug("Cleaning resources")

        if "db_session" in data:
            self._logger.debug("SQLAlchemy session detected, closing connection.")
            session: AsyncSession = data["db_session"]
            await session.commit()  # Commit changes
            await session.close()

        if "rtsu" in data:
            self._logger.debug("RTSU API Client detected, closing resource.")
            api_client: RTSUApi = data["rtsu"]
            await api_client.close_session()

    async def on_pre_process_message(self, update: types.Message, data: dict):
        """
        For pre-processing `types.Update`
        :param data: Data from other middlewares
        :param update: A telegram-update
        :return:
        """
        await update.bot.send_chat_action(update.from_user.id, "typing")
        resources = await self._provide_resources()

        data.update(resources)

        return data

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        """
        Method for preprocessing callback-queries
        :param query: A callback-query
        :param data: A data from another middleware
        :return:
        """

        resources = await self._provide_resources()

        data.update(resources)

        return data

    async def on_post_process_callback_query(self, query: types.CallbackQuery, data_from_handler: list, data: dict):
        """
        Method for post-processing callback query
        :param data_from_handler: Data from handler
        :param query: A callback query
        :param data: A data from another middleware
        :return:
        """

        await self._cleanup(data)

    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        """
        For post-processing message
        :param data_from_handler:
        :param message:
        :param data:
        :return:
        """
        await self._cleanup(data)
