from sqlalchemy import Integer, Column, String, Boolean

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=255), nullable=True)
    token = Column(String(length=600), nullable=True)
    is_authorized = Column(Boolean, default=False)
    telegram_id = Column(Integer)

    def __str__(self):
        return f"{self.__class__.__name__}<id={self.id}, name={self.full_name}>"
