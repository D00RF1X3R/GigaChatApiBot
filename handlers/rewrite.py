from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from keyboards.starter import keyboard
from database.user_db import user_data
from filters.is_rewriting import IsRewriting
from services.gigachatapi import ask

router = Router()

router.message.filter(IsRewriting())


@router.message()
async def chat(message: Message):
    res = await ask(message.text)
    await message.answer(text=res)
