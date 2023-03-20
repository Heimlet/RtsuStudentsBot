from aiohttp import ClientSession, ContentTypeError, client_exceptions
from cashews import cache
from typing import Optional, Union, Dict, TypeVar, Type, List, Self

from pydantic import BaseModel, parse_obj_as

from .exceptions import NotAuthorizedError, RtsuContentTypeError, ServerError, AuthError
from .schemas import AuthSchema, Profile, Subject, AcademicYear

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

    def set_token(self, token: str):
        """
        Setups token
        :param token: A token
        :return:
        """
        self._api_token = token

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
        :param url_part: Part of RTSU-API url, example - /auth
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

        try:
            response = await self._http_client.request(
                method,
                f"{RTSU_API_BASE_URL}/{url_part}",
                json=json,
                params=params,
                headers=headers,
                ssl=False,
            )
        except (client_exceptions.ClientConnectionError, client_exceptions.ClientConnectorError) as e:
            raise ServerError(f"Connection error, details: {e}")

        if response.status != 200:
            details = await response.text()
            raise ServerError(
                f"Server returned {response.status}, details: {details}"
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

        try:
            response: AuthSchema = await self._make_request(
                "POST",
                "auth",
                AuthSchema,
                params={
                    "login": login,
                    "password": password,
                }
            )
        except ServerError as e:
            raise AuthError(
                f"Auth error, check login and password, message from server: {e.message}"
            )

        self._api_token = response.token

        return response

    @cache.soft(ttl="24h", soft_ttl="1m")
    async def get_profile(self) -> Profile:
        """
        Returns profile of RTSU student
        :return: `Profile`-response
        """

        return await self._make_request(
            "GET",
            "student/profile",
            Profile,
            auth_required=True,
        )

    async def get_academic_years(self) -> List[AcademicYear]:
        """
        Returns `List` with `AcademicYear` objects
        :return:
        """

        return await self._make_request(
            "GET",
            "student/academic_years",
            List[AcademicYear],
            auth_required=True,
        )

    @cache.soft(ttl="24h", soft_ttl="1m")
    async def get_academic_year_subjects(self, year_id: int) -> List[Subject]:
        """
        Returns `List` with `Subjects` of some year
        :return:
        """

        return await self._make_request(
            "GET",
            f"student/grades/{year_id}",
            List[Subject],
            auth_required=True,
        )

    async def get_current_year_id(self) -> int:
        """
        Returns identifier of current year
        :return:
        """

        years = await self.get_academic_years()

        return years[0].id

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    def __str__(self) -> str:
        """
        Stringifies `RTSUApi` objects
        :return:
        """

        return f"{self.__class__.__name__}<token={self._api_token}>"

    async def close_session(self):
        """Frees inner resources"""
        await self._http_client.close()
