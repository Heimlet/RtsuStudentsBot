from typing import Optional

from pydantic import BaseSettings

from .constants import DEFAULT_ENCODING, SETTINGS_FILE


class DatabaseSettings(BaseSettings):
    """Settings of database"""
    url: str


class BotSettings(BaseSettings):
    """Settings of telegram-bot"""
    token: str


class Logging(BaseSettings):
    format: str
    debug: bool


class Webhooks(BaseSettings):
    host: str
    path: str
    webapp_host: str
    webapp_port: int


class Settings(BaseSettings):
    """Class for settings"""
    bot: BotSettings
    logging: Logging
    db: DatabaseSettings
    webhooks: Optional[Webhooks] = None


settings = Settings.parse_file(
    path=SETTINGS_FILE,
    encoding=DEFAULT_ENCODING
)
