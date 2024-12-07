from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

router = Router()