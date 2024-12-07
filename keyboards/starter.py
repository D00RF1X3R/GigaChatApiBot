from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_builder = ReplyKeyboardBuilder()
adm_kb_builder = ReplyKeyboardBuilder()
rewrite_btn = KeyboardButton(text='Начать рерайтинг')
help_btn = KeyboardButton(text='Помощь')
author_btn = KeyboardButton(text='Автор')
donate_btn = KeyboardButton(text='Дать денег')
admin = KeyboardButton(text='Админка')

kb_builder.row(*[rewrite_btn, help_btn, author_btn, donate_btn], width=4)
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_builder.row(*[rewrite_btn, help_btn, author_btn, donate_btn], width=4)
kb_builder.row(admin, width=1)
admin_kb: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
)
