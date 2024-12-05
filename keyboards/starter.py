from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_builder = ReplyKeyboardBuilder()
rewrite_btn = KeyboardButton(text='Переписать текст')
survey_btn = KeyboardButton(text='Пройти опрос')
quiz_1_btn = KeyboardButton(text='Викторина 1')
quiz_2_btn = KeyboardButton(text='Викторина 2')

kb_builder.row(rewrite_btn, width=1)
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

