import logging

from typing import Any
from sqlalchemy.orm import declarative_base
from typing import List, Tuple

from sqlalchemy import Column, Integer, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

Base = declarative_base()


class BaseModelFunctionality:
    """
    Base functionality of any model.
    """
    id = Column(Integer, primary_key=True)

    @classmethod
    def _validate_fields(cls, fields: dict):
        """
        Validates given fields
        :param fields: A dictionary with fields
        """

        for field in fields:
            if not hasattr(cls, field):
                raise ValueError(f"Class '{cls.__name__}' don't have field '{field}'")

    @classmethod
    async def create(
            cls: Any,
            session: AsyncSession,
            **kwargs
    ) -> Tuple[Any, bool]:
        """Creates object."""

        cls._validate_fields(kwargs)

        obj = cls(**kwargs)

        session.add(obj)

        try:
            await session.flush()
        except Exception as e:
            logging.error(f"Can't create {obj}, {e}")
            return obj, False

        return obj, True

    @classmethod
    async def delete(cls, session: AsyncSession, object_id: int) -> bool:
        """
        Deletes object by identifier
        :param session: An `AsyncSession` object
        :param object_id: Object's ID
        :return: `True` if object deleted successfully
        """
        try:
            await session.delete(object_id)
        except Exception as e:
            logging.error(f"Deleting error, {e}")
            return False
        return True

    @classmethod
    async def update(cls, session: AsyncSession, object_id: int, **kwargs) -> bool:
        """
        Updates object by ID
        :param session: An `AsyncSession` object
        :param object_id: Object's ID
        :param kwargs: Keyword-arguments
        :return: `True` if object updated successfully
        """
        cls._validate_fields(kwargs)

        query = update(cls).where(cls.id == object_id).values(
            **kwargs
        )

        await session.execute(query)

        try:
            await session.flush()
        except Exception as e:
            logging.error(f"Updating error, {e}")
            return False

        return True

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs) -> List[Any]:
        """
        Filters & returns objects.
        :param session: An `AsyncSession` object
        :param kwargs: A kwargs
        :return: List with `cls` objects
        """
        cls._validate_fields(kwargs)

        query = select(cls)

        for key in kwargs:
            value = kwargs.get(key)

            query = query.where(
                getattr(cls, key) == value
            )

        a = await session.execute(query)

        return a.scalars().all()
