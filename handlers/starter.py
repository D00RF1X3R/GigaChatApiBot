from aiogram import Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram_dialog import DialogManager

from states.rewriting import FSMRewrite
from states.authortab import FSMAuthor

from lexicon.lexicon import LEXICON
from keyboards.starter import keyboard

from database.orm import insert_data

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await insert_data(message.from_user.id)
    print(message.chat.id)
    await message.answer(text=LEXICON['/start'], reply_markup=keyboard)


@router.message(lambda message: message.text == "Помощь", StateFilter(default_state))
async def process_help(message: Message):
    await message.answer(text=LEXICON["help"], reply_markup=keyboard)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["help"], reply_markup=keyboard)


@router.message(lambda message: message.text == "Автор", StateFilter(default_state))
async def process_author(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await state.set_state(FSMAuthor.in_author_tab)
    await dialog_manager.start(FSMAuthor.in_author_tab)


@router.message(StateFilter(FSMAuthor.in_author_tab))
async def leave_author(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON['greeting'], reply_markup=keyboard)


@router.message(lambda message: message.text == "Начать рерайтинг", StateFilter(default_state))
async def rewrite(message: Message, state: FSMContext):
    await state.set_state(FSMRewrite.rewriting)
    await message.answer(text="Поехали!")
