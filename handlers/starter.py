from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from keyboards.starter import keyboard
from database.user_db import user_data

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    user_data[message.from_user.id] = {"rewriting": False}
    await message.answer(text=LEXICON['/start'], reply_markup=keyboard)


@router.message(lambda message: message.text == "Переписать текст")
async def rewrite(message: Message):
    user_data[message.from_user.id]["rewriting"] = True
    await message.answer(text="Поехали!")


