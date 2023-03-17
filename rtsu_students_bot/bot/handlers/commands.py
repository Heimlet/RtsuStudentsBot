from aiogram import types, Dispatcher

from rtsu_students_bot.bot.templates import welcome


async def start(message: types.Message):
    """
    Handles `/start` cmd
    :param message: A message
    """

    await message.reply(
        welcome.substitute(
            user=message.from_user.full_name
        )
    )


def setup(dp: Dispatcher):
    """
    Setups commands-handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=["start"])
