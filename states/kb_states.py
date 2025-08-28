from aiogram.fsm.state import StatesGroup, State

# Состояния для FSM
class AuthStates(StatesGroup):
    waiting_for_email = State()

class AddKnowledge(StatesGroup):
    waiting_for_text = State()

class SearchKnowledge(StatesGroup):
    waiting_for_query = State()