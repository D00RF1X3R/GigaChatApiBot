from aiogram import Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.rewriting import FSMRewrite

from lexicon.lexicon import LEXICON
from keyboards.starter import keyboard

from database.orm import insert_data, change_rewriting


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await insert_data(message.from_user.id)
    await message.answer(text=LEXICON['/start'], reply_markup=keyboard)


@router.message(lambda message: message.text == "Переписать текст", StateFilter(default_state))
async def rewrite(message: Message, state: FSMContext):
    await change_rewriting(message.from_user.id)
    await state.set_state(FSMRewrite.rewriting)
    await message.answer(text="Поехали!")


