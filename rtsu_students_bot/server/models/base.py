import logging

from typing import Self, Any, TypeVar
from sqlalchemy.orm import declarative_base
from typing import List, Optional, Tuple

from sqlalchemy import Column, String, Integer, update, Text
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
        """Deletes object by ID"""
        try:
            await session.delete(object_id)
        except Exception as e:
            logging.error(f"Deleting error, {e}")
            return False
        return True

    @classmethod
    async def update(cls):
        raise NotImplementedError

    @classmethod
    async def get(cls):
        raise NotImplementedError
