import logging

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states.rewriting import FSMRewrite

from keyboards.prerewritekb import pre_rewrite_kb
from keyboards.historykb import left_inline_kb, right_inline_kb, double_inline_kb, HistoryCallbackFactory, cross_kb
from keyboards.starter import keyboard, admin_kb

from lexicon.lexicon import LEXICON

from database.orm import get_rewrites, remove_rewrite, remove_all_rewrites

router = Router()
logger = logging.getLogger(__name__)


@router.message(lambda message: message.text == "Начать перепись", StateFilter(FSMRewrite.pre_rewrite))
async def process_rewriting(message: Message, state: FSMContext):
    await state.set_state(FSMRewrite.rewriting)
    await message.answer(text='Напишите то, что хотели бы переписать', reply_markup=ReplyKeyboardRemove())
    logger.info("Пользователь вошел в меню переписей.")


@router.message(lambda message: message.text == "Вернуться в начало", StateFilter(FSMRewrite.pre_rewrite))
async def process_leave(message: Message, state: FSMContext, user):
    await state.clear()
    if user == "admin":
        await message.answer(text=LEXICON["admin_greet"], reply_markup=admin_kb)
    else:
        await message.answer(text=LEXICON["greeting"], reply_markup=keyboard)
    logger.info("Пользователь вышел из истории переписей.")


@router.message(lambda message: message.text == "История переписей", StateFilter(FSMRewrite.pre_rewrite))
async def process_rewrite_history(message: Message, state: FSMContext):
    await state.set_state(FSMRewrite.history)
    res = await get_rewrites(message.from_user.id)
    await state.update_data({"curr_var": 0})
    await state.update_data({"variants": res})
    if res:
        await message.answer(text=res[0], reply_markup=right_inline_kb)
    else:
        await state.set_state(FSMRewrite.pre_rewrite)
        await message.answer(text='У вас пока нет переписей.', reply_markup=pre_rewrite_kb)
    logger.info("Пользователь вошел в историю переписей.")


@router.message(lambda message: message.text == "Удалить историю", StateFilter(FSMRewrite.pre_rewrite))
async def process_history_clean(message: Message):
    await remove_all_rewrites(message.from_user.id)
    await message.answer(text='История переписей очищена.', reply_markup=pre_rewrite_kb)
    logger.info("Пользователь очистил историю переписей.")


@router.callback_query(HistoryCallbackFactory.filter(F.next_move == 2), StateFilter(FSMRewrite.history))
async def process_right_arrow(callback: CallbackQuery, state: FSMContext):
    curr_var = (await state.get_data())["curr_var"]
    variants = (await state.get_data())["variants"]
    if curr_var + 1 == len(variants) - 1:
        await callback.message.edit_text(text=variants[curr_var + 1], reply_markup=left_inline_kb)
        await state.update_data({"curr_var": curr_var + 1})
    else:
        await callback.message.edit_text(text=variants[curr_var + 1], reply_markup=double_inline_kb)
        await state.update_data({"curr_var": curr_var + 1})
    logger.info("Пользователь нажал стрелку вправо.")
    await callback.answer()


@router.callback_query(HistoryCallbackFactory.filter(F.next_move == 1), StateFilter(FSMRewrite.history))
async def process_left_arrow(callback: CallbackQuery, state: FSMContext):
    curr_var = (await state.get_data())["curr_var"]
    variants = (await state.get_data())["variants"]
    if curr_var - 1 == 0:
        await callback.message.edit_text(text=variants[curr_var - 1], reply_markup=right_inline_kb)
        await state.update_data({"curr_var": curr_var - 1})
    else:
        await callback.message.edit_text(text=variants[curr_var - 1], reply_markup=double_inline_kb)
        await state.update_data({"curr_var": curr_var - 1})
    logger.info("Пользователь нажал стрелку влево.")
    await callback.answer()


@router.callback_query(HistoryCallbackFactory.filter(F.next_move == 3), StateFilter(FSMRewrite.history))
async def process_remove_variant(callback: CallbackQuery, state: FSMContext):
    curr_var = (await state.get_data())["curr_var"]
    variants = (await state.get_data())["variants"]
    await remove_rewrite(callback.from_user.id, variants[curr_var])
    variants.pop(curr_var)
    if len(variants) == 0:
        await callback.message.edit_text(text="Переписи закончились.", reply_markup=cross_kb)
    elif curr_var == 0:
        await callback.message.edit_text(text=variants[curr_var], reply_markup=right_inline_kb)
    elif curr_var == len(variants):
        await callback.message.edit_text(text=variants[curr_var - 1], reply_markup=left_inline_kb)
        await state.update_data({"curr_var": curr_var - 1})
    else:
        await callback.message.edit_text(text=variants[curr_var], reply_markup=double_inline_kb)
    await state.update_data({"variants": variants})
    logger.info("Перепсись удалена.")
    await callback.answer("Успешно удалено")


@router.callback_query(HistoryCallbackFactory.filter(F.next_move == 0), StateFilter(FSMRewrite.history))
async def process_cancel(callback: CallbackQuery, state: FSMContext, user):
    await callback.message.edit_reply_markup(None)
    await state.clear()
    if user == "admin":
        await callback.message.answer(text=LEXICON["admin_greet"], reply_markup=admin_kb)
    else:
        await callback.message.answer(text=LEXICON["greeting"], reply_markup=keyboard)
    await callback.answer()
    logger.info("Пользователь вышел из истории переписей.")
