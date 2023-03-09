from aiohttp import ClientSession, ContentTypeError

from typing import Optional, Union, Dict, TypeVar, Type, List, Self

from pydantic import BaseModel, parse_obj_as

from .exceptions import NotAuthorizedError, RtsuContentTypeError
from .schemas import AuthSchema

RTSU_API_BASE_URL = "https://mobile.rtsu.tj/api/v1"
P = TypeVar("P", bound=BaseModel)


class RTSUApi:
    """
    This class provides for you functionality of RTSU public API
    """

    def __init__(self, token: Optional[str] = None):
        """
        Initializes `self`
        :param token: A rtsu-api token (optional)
        """

        self._api_token = token
        self._http_client = ClientSession()

    async def _make_request(
            self,
            method: str,
            url_part: str,
            response_model: Type[Union[List[BaseModel], BaseModel]],
            json: Optional[Dict[str, Union[str, int]]] = None,
            params: Optional[Dict[str, str]] = None,
            auth_required: bool = False,
    ) -> Union[P, List[P]]:
        """
        Makes call to RTSU API
        :param url_part: Part of RTSU-API url, example - `/auth`
        :param json: A json for sending
        :param params: URI parameters for sending
        :return: Response object
        """

        if not json:
            json = {}

        if not params:
            params = {}

        headers = {}

        if auth_required:
            if not self._api_token:
                raise NotAuthorizedError("Not authorized, use `.auth` method.")

            headers['token'] = self._api_token

        response = await self._http_client.request(
            method,
            f"{RTSU_API_BASE_URL}/{url_part}",
            json=json,
            params=params,
            headers=headers,
            ssl=False,
        )

        try:
            deserialized_data = await response.json()
        except ContentTypeError as e:
            raise RtsuContentTypeError(
                e.message,
            )

        return parse_obj_as(response_model, deserialized_data)

    async def auth(self, login: str, password: str) -> AuthSchema:
        """
        Authenticates user
        :param login: A login of user
        :param password: A password of user
        :return: RTSU token on success
        """

        response: AuthSchema = await self._make_request(
            "POST",
            "auth",
            AuthSchema,
            params={
                "login": login,
                "password": password,
            }
        )

        self._api_token = response.token

        return response

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    async def close_session(self):
        """Frees inner resources"""
        await self._http_client.close()
