from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_builder = ReplyKeyboardBuilder()

history_button = KeyboardButton(text="История рерайтов")
history_delete_button = KeyboardButton(text="Удалить историю")
rewrite_button = KeyboardButton(text="Начать рерайт")
back_button = KeyboardButton(text="Вернуться в начало")

# Клавиатура для страницы рерайтов
kb_builder.row(*[rewrite_button, history_button, history_delete_button, back_button], width=4)
pre_rewrite_kb = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)
