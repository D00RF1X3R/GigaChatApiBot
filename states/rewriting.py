from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMRewrite(StatesGroup):
    pre_rewrite = State()
    history = State()
    rewriting = State()
    rewrote = State()
