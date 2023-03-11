import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from rtsu_students_bot.service import user
from rtsu_students_bot.models import Base

from .config import settings

pytest_plugins = ('pytest_asyncio',)

engine = create_async_engine(
    settings.db_url,
)

SessionLocal = sessionmaker(autoflush=True, bind=engine, class_=AsyncSession)


@pytest_asyncio.fixture()
async def session():
    """
    Initializes client
    :return: Prepared `RTSUApi` client
    """

    async with SessionLocal() as e, e.begin():
        yield e


@pytest.mark.asyncio
async def test_tables_creating():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_user_creation(session: AsyncSession):
    """
    Tests user-creation
    :return:
    """

    user_data = {
        "full_name": "Vladimir Putin",
        "telegram_id": 1,
    }

    created_user = await user.create_user(session, **user_data)

    assert created_user.full_name == user_data.get("full_name")
    assert created_user.telegram_id == user_data.get("telegram_id")


@pytest.mark.asyncio
async def test_user_update(session: AsyncSession):
    """
    Tests user updating
    :param session:
    :return:
    """

    updating_data = {
        "full_name": "Volodymir Zelensky"
    }

    first_user = await user.get_user_by_tg_id(session, 1)

    updated_user = await user.update_user(session, first_user.id, **updating_data)

    assert first_user.id == updated_user.id
    assert first_user.telegram_id == updated_user.telegram_id
    assert updated_user.full_name == updating_data.get("full_name")


@pytest.mark.asyncio
async def test_user_token_updating(session: AsyncSession):
    """
    Tests user-token updating
    :param session:
    :return:
    """

    first_user = await user.get_user_by_tg_id(session, 1)

    assert not first_user.is_authorized

    first_user = await user.update_user_token(session, first_user.telegram_id, token="test token")

    assert first_user.is_authorized
    assert first_user.token == "test token"
    assert first_user.telegram_id == 1


@pytest.mark.asyncio
async def test_user_deleting(session: AsyncSession):
    """
    Tests user-token updating
    :param session:
    :return:
    """

    first_user = await user.get_user_by_tg_id(session, 1)

    assert first_user is not None

    await user.delete_user(session, first_user.id)

    first_user = await user.get_user_by_tg_id(session, 1)

    assert first_user is None
