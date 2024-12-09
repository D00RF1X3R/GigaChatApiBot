from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMAuthor(StatesGroup):  # Машина состояний для перехода в страницу авторов
    in_author_tab = State()
