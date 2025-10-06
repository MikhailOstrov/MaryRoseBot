from aiogram.fsm.state import State, StatesGroup

class UserAuthStatus(StatesGroup):
    authorized = State()
    unauthorized = State()