import pytest
import pytest_asyncio

from rtsu_students_bot.rtsu import RTSUApi

pytest_plugins = ('pytest_asyncio',)

TEST_DATA = {
    "login": "your login",
    "password": "your pass",
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


@pytest.mark.asyncio
async def test_rtsu_profile_fetching(rtsu_client: RTSUApi):
    """
    Tests rtsu profile fetching
    :param rtsu_client:
    :return:
    """

    await rtsu_client.auth(TEST_DATA.get("login"), TEST_DATA.get("password"))

    profile = await rtsu_client.get_profile()

    assert profile is not None
    assert profile.full_name is not None


@pytest.mark.asyncio
async def test_rtsu_academic_years_fetching(rtsu_client: RTSUApi):
    """
    Tests rtsu academic years fetching
    :param rtsu_client:
    :return:
    """

    await rtsu_client.auth(TEST_DATA.get("login"), TEST_DATA.get("password"))

    years = await rtsu_client.get_academic_years()

    assert type(years) == list
    assert len(years) > 0


@pytest.mark.asyncio
async def test_rtsu_academic_year_subjects_fetching(rtsu_client: RTSUApi):
    """
    Tests rtsu academic year fetching
    :param rtsu_client:
    :return:
    """

    await rtsu_client.auth(TEST_DATA.get("login"), TEST_DATA.get("password"))

    ac_years = await rtsu_client.get_academic_years()
    year = ac_years[0].id
    years = await rtsu_client.get_academic_year_subjects(year)

    assert type(years) == list
    assert len(years) > 0
