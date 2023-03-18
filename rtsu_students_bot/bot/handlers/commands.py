from aiogram import types, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from rtsu_students_bot.models import User
from rtsu_students_bot.bot.keyboards import inline
from rtsu_students_bot.template_engine import render_template


async def start(message: types.Message, user: User):
    """
    Handles `/start` cmd
    :param user:
    :param message: A message
    """

    await message.reply(
        text=render_template(
            "start.html",
            user=message.from_user.full_name,
            telegram_id=message.from_user.id,
            user_id=user.id,
        ),
        reply_markup=inline.start_keyboard_factory()
    )


def setup(dp: Dispatcher):
    """
    Setups commands-handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=["start"])
