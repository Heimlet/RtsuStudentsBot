from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...common import schemas

from ..models import User

from .dependencies import session_factory

router = APIRouter(prefix='/users')


@router.get(
    "/",
    description="Returns list with `User` objects.",
    summary="Get users",
    response_model=List[schemas.out.User]
)
async def get_users(
        id_: Optional[int] = Query(title="ID in db", alias="id", description="Filter by ID", default=None),
        telegram_id: Optional[int] = Query(title="Telegram's ID", description="Filter by telegram-id", default=None),
        login: Optional[str] = Query(title="RTSU Login", description="Login (RTSU)", default=None),
        session: AsyncSession = Depends(session_factory)
):
    """
    Filters & returns users
    :param id_: ID of user (optional)
    :param telegram_id: Telegram-ID of user (optional)
    :param login: Login of user (optional)
    :param session: AsyncSession object (dependency)
    """
    statement = select(User)

    if id_:
        statement = statement.where(
            id == id_
        )

    if telegram_id:
        statement = statement.where(
            telegram_id == telegram_id
        )

    if login:
        statement = statement.where(
            login == login,
        )

    result = await session.execute(
        statement
    )

    return result.scalars().all()


@router.get(
    "/{user_id}",
    description="Returns `User` by its ID.",
    summary="Get user by id",
    response_model=schemas.out.User
)
async def get_user_by_id(
        id_: int = Path(title="User's ID", description="ID of user in database"),
        session: AsyncSession = Depends(session_factory),
):
    """
    Returns user by its ID
    :param id_: A user's ID
    :param session: AsyncSession object (Dependency)
    """
    result = await session.execute(
        select(
            User
        ).where(
            id == id_
        )
    )

    return result.scalars().first()
