from pydantic import Field

from .base import Base


class AuthSchema(Base):
    token: str = Field(alias='message')
