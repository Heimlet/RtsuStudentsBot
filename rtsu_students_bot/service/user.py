from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.models import User

from .exceptions import UserNotFound, UserAlreadyExists


async def get_user_by_tg_id(
        session: AsyncSession,
        telegram_id: int,
) -> Optional[User]:
    """
    Returns user by tg-id
    :param session: An `AsyncSession` object
    :param telegram_id: A telegram-ID
    :return: `User` or `None`
    """

    stmt = select(User).where(User.telegram_id == telegram_id)

    result = await session.execute(stmt)

    return result.scalars().first()


async def get_user_by_id(
        session: AsyncSession,
        user_id: int,
) -> Optional[User]:
    """
    Returns user by its id
    :param session: An `AsyncSession` object
    :param user_id: An ID
    :return: `User` or `None`
    """

    stmt = select(User).where(User.id == user_id)

    result = await session.execute(stmt)

    return result.scalars().first()


async def create_user(
        session: AsyncSession,
        telegram_id: int,
        full_name: Optional[str] = None,
        token: Optional[str] = None,
):
    """
    Creates `User` object
    :param session: An `AsyncSession` object
    :param telegram_id: A telegram-id
    :param full_name: Fullname of user
    :param token: A token of user
    :return: Created `User`
    """

    existed_user = await get_user_by_tg_id(session, telegram_id)

    if existed_user is not None:
        raise UserAlreadyExists(f"User with ID {telegram_id} already exists.")

    is_authorized = token is not None

    obj = User(
        telegram_id=telegram_id,
        full_name=full_name,
        token=token,
        is_authorized=is_authorized,
    )

    session.add(obj)
    await session.flush()
    await session.refresh(obj)

    return obj


async def update_user_token(
        session: AsyncSession,
        telegram_id: int,
        token: Optional[str] = None,
) -> User:
    """
    Authorizes `User`
    :param telegram_id:
    :param session:
    :param token:
    :return:
    """

    user = get_user_by_tg_id(session, telegram_id)

    if not user:
        raise UserNotFound("User not found.")

    is_authorized = token is not None
    stmt = update(User).values(token=token, is_authorized=is_authorized)

    await session.execute(stmt)

    return await get_user_by_tg_id(session, telegram_id)


async def update_user(
        user_id: int,
        session: AsyncSession,
        telegram_id: Optional[int] = None,
        full_name: Optional[str] = None,
) -> User:
    """
    Updates telegram user
    :param session:
    :param user_id:
    :param telegram_id:
    :param full_name:
    :return:
    """

    user = await get_user_by_id(session, user_id)

    if not user:
        raise UserNotFound(f"User with ID {user_id} not found.")

    stmt = update(User).where(User.id == user_id)

    if telegram_id is not None:
        stmt.values(
            telegram_id=telegram_id,
        )

    if full_name is not None:
        stmt.values(
            full_name=full_name
        )

    await session.execute(stmt)

    return await get_user_by_id(session, user_id)
