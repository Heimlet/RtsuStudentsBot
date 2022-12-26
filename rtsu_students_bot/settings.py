from pydantic import BaseSettings


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


class Settings(BaseSettings):
    """Class for settings"""
    server: ServerSettings
    bot: BotSettings
