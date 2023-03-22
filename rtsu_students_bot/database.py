from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from rtsu_students_bot.config import settings

engine = create_async_engine(
    settings.db.url,
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
