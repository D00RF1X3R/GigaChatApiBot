from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMRewrite(StatesGroup):
    rewriting = State()
    rewrote = State()