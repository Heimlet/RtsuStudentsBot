import pytest
import pytest_asyncio

from rtsu_students_bot.rtsu import RTSUApi

from .config import settings

pytest_plugins = ('pytest_asyncio',)


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

    resp = await rtsu_client.auth(settings.rtsu_api_login, settings.rtsu_api_password)

    assert resp.token is not None

    with open("some.txt", 'w') as f:
        f.write(resp.token)


@pytest.mark.asyncio
async def test_rtsu_profile_fetching(rtsu_client: RTSUApi):
    """
    Tests rtsu profile fetching
    :param rtsu_client:
    :return:
    """

    await rtsu_client.auth(settings.rtsu_api_login, settings.rtsu_api_password)

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

    await rtsu_client.auth(settings.rtsu_api_login, settings.rtsu_api_password)

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

    await rtsu_client.auth(settings.rtsu_api_login, settings.rtsu_api_password)

    ac_years = await rtsu_client.get_academic_years()
    year = ac_years[0].id
    years = await rtsu_client.get_academic_year_subjects(year)

    assert type(years) == list
    assert len(years) > 0
