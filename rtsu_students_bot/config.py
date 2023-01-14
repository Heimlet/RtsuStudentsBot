from pydantic import BaseSettings

from .constants import DEFAULT_ENCODING, SETTINGS_FILE


class DatabaseSettings(BaseSettings):
    """Settings of database"""
    url: str


class BotSettings(BaseSettings):
    """Settings of telegram-bot"""
    token: str


class ServerSettings(BaseSettings):
    """Settings of server"""
    host: str
    port: int
    db: DatabaseSettings


class Logging(BaseSettings):
    format: str
    debug: bool


class Settings(BaseSettings):
    """Class for settings"""
    server: ServerSettings
    bot: BotSettings
    logging: Logging


settings = Settings.parse_file(
    path=SETTINGS_FILE,
    encoding=DEFAULT_ENCODING
)
