from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMAuthor(StatesGroup):
    in_author_tab = State()
