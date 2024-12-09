from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_builder = ReplyKeyboardBuilder()
adm_kb_builder = ReplyKeyboardBuilder()
next_kb_builder = ReplyKeyboardBuilder()
next_btn = KeyboardButton(text='Продолжить')
rewrite_btn = KeyboardButton(text='Начать рерайтинг')
help_btn = KeyboardButton(text='Помощь')
author_btn = KeyboardButton(text='Автор')
donate_btn = KeyboardButton(text='Дать денег')
admin = KeyboardButton(text='Админка')

kb_builder.row(*[rewrite_btn, help_btn, author_btn, donate_btn], width=4)  # Основаня клавиатура
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

adm_kb_builder.row(*[rewrite_btn, help_btn, author_btn, donate_btn], width=4)
adm_kb_builder.row(admin, width=1)  # Основаня клавиатура для админа
admin_kb: ReplyKeyboardMarkup = adm_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
)

next_kb_builder.row(next_btn, width=1)  # Клавиатура продолжения
next_kb: ReplyKeyboardMarkup = next_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
)
