from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMAdmin(StatesGroup):
    admin = State()
    banned_users = State()
    users = State()
    counts = State()
