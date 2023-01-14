from enum import Enum as PythonEnum

from sqlalchemy import Column, String, Integer, Enum

from .base import Base


class UserRole(PythonEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    CREATOR = "CREATOR"


class User(Base):
    """Users table"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    login = Column(String)
    password = Column(String)
    rtsu_token = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
