from aiogram.dispatcher.filters.state import StatesGroup, State


class AuthState(StatesGroup):
    login = State()
    password = State()
    confirm = State()
