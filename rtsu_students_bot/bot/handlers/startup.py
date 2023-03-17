from aiogram import types, Dispatcher

BOT_COMMANDS = [
    types.BotCommand(
        "start",
        "Старт бота"
    )
]


async def startup_handler(dp: Dispatcher):
    """
    Startup handler
    :return:
    """

    await dp.bot.set_my_commands(
        BOT_COMMANDS
    )
