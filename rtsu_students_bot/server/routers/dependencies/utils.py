from sqlalchemy.ext.asyncio import AsyncSession
from ...database import SessionLocal


async def session_factory() -> AsyncSession:
    """
    Dependency, inject it for getting an `AsyncSession`-object.
    """

    async with SessionLocal() as e, e.begin():
        yield e
