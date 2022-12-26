from enum import Enum as PythonEnum

from sqlalchemy import Column, String, Integer, Enum

from .base import Base, BaseModelFunctionality


class UserRole(PythonEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    CREATOR = "CREATOR"


class User(Base, BaseModelFunctionality):
    """For user"""
    __table__ = 'users'
    telegram_id = Column(Integer)
    login = Column(String)
    password = Column(String)
    token = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
