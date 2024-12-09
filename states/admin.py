from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMAdmin(StatesGroup):  # Машина состояний для перехода в страницу админа
    admin = State()
    banned_users = State()
    users = State()
    counts = State()
