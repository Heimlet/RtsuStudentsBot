from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from . import callbacks


def start_keyboard_factory() -> InlineKeyboardMarkup:
    """
    Builds & returns keyboard for `/start` cmd
    :return:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Авторизация",
            callback_data=callbacks.AUTH_CALLBACK.new()
        )
    )

    return keyboard
