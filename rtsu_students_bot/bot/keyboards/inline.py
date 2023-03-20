from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from rtsu_students_bot.rtsu import schemas

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


def subjects_keyboard_factory(subjects: List[schemas.Subject]) -> InlineKeyboardMarkup:
    """
    Builds & returns keyboards with list of subjects
    :param subjects: List of subjects
    :return: Prepared keyboard with subjects
    """

    markup = InlineKeyboardMarkup()

    for subj in subjects:
        markup.add(
            InlineKeyboardButton(
                text=subj.name.ru,
                callback_data=callbacks.SUBJECT_CALLBACK.new(subj.id)
            )
        )

    return markup


def message_hiding_keyboard() -> InlineKeyboardMarkup:
    """
    Builds keyboard for message-deleting
    :return:
    """

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "🔽 Скрыть", callback_data=callbacks.DELETE_MSG_CALLBACK.new()
        )
    )

    return markup
