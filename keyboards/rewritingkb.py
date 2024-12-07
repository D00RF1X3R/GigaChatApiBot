from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class RewrittenCallbackFactory(CallbackData, prefix='next move'):
    next_move: int


button_save = InlineKeyboardButton(
    text='💾',
    callback_data=RewrittenCallbackFactory(next_move=1).pack(),
)

button_re_rewrite = InlineKeyboardButton(
    text='🔁',
    callback_data=RewrittenCallbackFactory(next_move=2).pack(),
)

button_rewrite_another = InlineKeyboardButton(
    text='🆕',
    callback_data=RewrittenCallbackFactory(next_move=3).pack()
)

button_back = InlineKeyboardButton(
    text='❌',
    callback_data=RewrittenCallbackFactory(next_move=0).pack()
)

button_left = InlineKeyboardButton(
    text="<<",
    callback_data=RewrittenCallbackFactory(next_move=4).pack()
)

button_right = InlineKeyboardButton(
    text='>>',
    callback_data=RewrittenCallbackFactory(next_move=5).pack()
)

single_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_save], [button_re_rewrite, button_rewrite_another],
                                                         [button_back]])

double_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_save], [button_re_rewrite, button_rewrite_another],
                                                         [button_left, button_right], [button_back]])

left_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_save], [button_re_rewrite, button_rewrite_another],
                                                       [button_left], [button_back]])

right_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[button_save], [button_re_rewrite, button_rewrite_another],
                                                        [button_right], [button_back]])
