import pytest
import pytest_asyncio

from rtsu_students_bot.rtsu import RTSUApi

pytest_plugins = ('pytest_asyncio',)

TEST_DATA = {
    "login": "YOUR LOGIN FOR TESTING",
    "password": "YOUR PASSWORD FOR TESTING",
}


@pytest_asyncio.fixture()
async def rtsu_client():
    """
    Initializes client
    :return: Prepared `RTSUApi` client
    """

    async with RTSUApi() as api:
        yield api


@pytest.mark.asyncio
async def test_rtsu_login(rtsu_client: RTSUApi):
    """
    Tests rtsu login
    :param rtsu_client: A RTSU API client
    :return:
    """

    resp = await rtsu_client.auth(TEST_DATA.get("login"), TEST_DATA.get("password"))

    assert resp.token is not None
