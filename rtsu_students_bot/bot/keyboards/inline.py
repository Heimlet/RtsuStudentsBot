from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from . import callbacks


def auth_keyboard_factory() -> InlineKeyboardMarkup:
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


def cancellation_keyboard_factory() -> InlineKeyboardMarkup:
    """
    Builds & returns keyboard for cancellation operations
    :return:
    """

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="Отмена операции",
            callback_data=callbacks.CANCELLATION_CALLBACK.new()
        )
    )

    return markup


def confirmation_keyboard_factory() -> InlineKeyboardMarkup:
    """
    Builds & returns keyboard for confirming credentials.
    :return:
    """

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("Да", callback_data=callbacks.CONFIRMATION_CALLBACK.new(1))
    )

    markup.add(
        InlineKeyboardButton("Нет", callback_data=callbacks.CONFIRMATION_CALLBACK.new(0))
    )

    return markup
