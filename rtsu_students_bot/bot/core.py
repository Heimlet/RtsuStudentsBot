from typing import Union, Optional
from aiogram import types

from .dispatcher import bot


async def send_text_message(
        chat_id: int,
        text: str,
        keyboard: Optional[Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]] = None
):
    """
    Sends a message
    :return:
    """

    await bot.send_message(
        chat_id,
        text=text,
        reply_markup=keyboard,
    )
