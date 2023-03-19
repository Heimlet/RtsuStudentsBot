from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def main_menu_factory() -> ReplyKeyboardMarkup:
    """
    Builds & returns keyboard with common bots functionality
    :return: Initialized `ReplyKeyboardMarkup`
    """

    markup = ReplyKeyboardMarkup()

    markup.row(
        KeyboardButton("📊 Статистика"),
        KeyboardButton("📕 Дисциплины"),
        KeyboardButton("🎓 Профиль"),
    )

    markup.row(
        KeyboardButton("🆘 Инструкция"),
        KeyboardButton("ℹ️ О боте"),
        KeyboardButton("🍩 Помощь проекту")
    )

    markup.row(
        KeyboardButton("🔑 Авторизация"),
        KeyboardButton("◀️ Выход из системы")
    )

    return markup
