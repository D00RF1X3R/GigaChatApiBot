from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class HistoryCallbackFactory(CallbackData, prefix='next move'):
    next_move: int


button_back = InlineKeyboardButton(
    text='❌',
    callback_data=HistoryCallbackFactory(next_move=0).pack()
)

button_left = InlineKeyboardButton(
    text='<<',
    callback_data=HistoryCallbackFactory(next_move=1).pack()
)

button_right = InlineKeyboardButton(
    text='>>',
    callback_data=HistoryCallbackFactory(next_move=2).pack()
)

button_remove = InlineKeyboardButton(
    text='🗑️',
    callback_data=HistoryCallbackFactory(next_move=3).pack()
)

left_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_left], [button_remove, button_back]])
right_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_right], [button_remove, button_back]])
double_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_left, button_right], [button_remove, button_back]])
cross_kb = InlineKeyboardMarkup(inline_keyboard=[[button_back]])






