from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class AdminCallbackFactory(CallbackData, prefix='admin_tab'):
    next_move: int | None
    id: int | None
    nick: str | None


def build_kb(users):
    builder = InlineKeyboardBuilder()
    if len(users) <= 100:
        for i in users:
            builder.button(text=f'{users[i]}',
                           callback_data=AdminCallbackFactory(id=i, nick=users[i], next_move=None).pack())
            builder.adjust(1, 1)
        builder.row(button_back, width=1)
        return builder.as_markup()
    else:
        return False


button_back = InlineKeyboardButton(
    text='❌',
    callback_data=AdminCallbackFactory(next_move=0, id=None, nick=None).pack()
)

button_ban_user = InlineKeyboardButton(
    text='Забанить пользователя',
    callback_data=AdminCallbackFactory(next_move=1, id=None, nick=None).pack()
)

button_unban_user = InlineKeyboardButton(
    text='Разбанить пользователя',
    callback_data=AdminCallbackFactory(next_move=2, id=None, nick=None).pack()
)

button_counts = InlineKeyboardButton(
    text='Счетчики',
    callback_data=AdminCallbackFactory(next_move=3, id=None, nick=None).pack()
)

admin_tab_kb = InlineKeyboardMarkup(
    inline_keyboard=[[button_ban_user, button_unban_user], [button_counts], [button_back]])
