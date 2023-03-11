from pydantic import BaseSettings

from rtsu_students_bot.constants import TEST_SETTINGS_FILE, DEFAULT_ENCODING


class Settings(BaseSettings):
    """Class for settings"""
    db_url: str
    rtsu_api_login: str
    rtsu_api_password: str


settings = Settings.parse_file(
    path=TEST_SETTINGS_FILE,
    encoding=DEFAULT_ENCODING
)
