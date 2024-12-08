import logging

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states.rewriting import FSMRewrite
from lexicon.lexicon import LEXICON, BAD_LEXICON
from keyboards.starter import keyboard
from keyboards.rewritingkb import (single_inline_kb, left_inline_kb,
                                   right_inline_kb, double_inline_kb, RewrittenCallbackFactory)
from services.gigachatapi import ask

from database.orm import insert_rewritten_text, check_text

router = Router()

logger = logging.getLogger(__name__)


@router.message(StateFilter(FSMRewrite.rewriting))
async def chat(message: Message, giga_key, state: FSMContext):
    res = await ask(message.text, giga_key)
    if res in BAD_LEXICON:
        await message.answer(text="Ваше сообщение содержит недопустимую информацию.",
                             reply_markup=ReplyKeyboardRemove())
        logger.info(f"Пользователь {message.from_user.username} написал что-то недопустимое")
    else:
        await state.set_state(FSMRewrite.rewrote)
        await state.set_data({"message": message.text})
        await state.update_data({"variant": 0})
        await state.update_data({"answers": [res]})
        logger.info(f"Успешный ответ пользователю {message.from_user.username}")
        await message.answer(text=res, reply_markup=single_inline_kb)


@router.message(StateFilter(FSMRewrite.rewrote))
async def working_with_old_one(message: Message):
    logger.info("Пользователь не завершил работу с прошлым текстом.")
    await message.answer(text="Сначала закончите работу с прошлой переписью.")


@router.callback_query(RewrittenCallbackFactory.filter(F.next_move == 1), StateFilter(FSMRewrite.rewrote))
async def process_save(callback: CallbackQuery):
    if not (await check_text(callback.from_user.id, callback.message.text)):
        await insert_rewritten_text(callback.from_user.id, callback.message.text)
        await callback.answer("Успешно сохранено")
        logger.info("Текст пользователя сохранен.")
    else:
        await callback.answer("Такая перепись уже есть")



@router.callback_query(RewrittenCallbackFactory.filter(F.next_move == 2), StateFilter(FSMRewrite.rewrote))
async def process_re_rewrite(callback: CallbackQuery, giga_key, state: FSMContext):
    res = await ask((await state.get_data())["message"], giga_key)
    if res in BAD_LEXICON:
        await state.clear()
        await state.set_state(FSMRewrite.rewriting)
        await callback.message.edit_text(text="Ваше сообщение содержит недопустимую информацию.")
        await callback.message.edit_reply_markup(None)
        await callback.message.answer(text=LEXICON["greeting"], reply_markup=ReplyKeyboardRemove())
        await callback.answer()
        logger.info(f"Текст пользователя {callback.from_user.username} содержит что-то недопустимое.")
    else:
        if res == callback.message.text:
            logger.info("Бот дал одинаковый ответ.")
            await callback.answer("Ничего нового не вышло.")
            return
        await state.update_data({"answers": [*(await state.get_data())["answers"], res]})
        await state.update_data({"variant": len((await state.get_data())["answers"]) - 1})
        await callback.message.edit_text(text=res, reply_markup=left_inline_kb)
        await callback.answer()
        logger.info(f"Текст пользователя {callback.from_user.username} переписан.")


@router.callback_query(RewrittenCallbackFactory.filter(F.next_move == 3), StateFilter(FSMRewrite.rewrote))
async def process_new_rewrite(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(None)
    await state.clear()
    await state.set_state(FSMRewrite.rewriting)
    await callback.message.answer(text="Продолжим!", reply_markup=ReplyKeyboardRemove())
    await callback.answer()
    logger.info("Начало работы с новым текстом.")


@router.callback_query(RewrittenCallbackFactory.filter(F.next_move == 4), StateFilter(FSMRewrite.rewrote))
async def process_left_variant(callback: CallbackQuery, state: FSMContext):
    variants = (await state.get_data())["answers"]
    curr_var = (await state.get_data())["variant"]
    await state.update_data({"variant": curr_var - 1})
    if curr_var - 1 == 0:
        await callback.message.edit_text(text=variants[curr_var - 1], reply_markup=right_inline_kb)

    else:
        await callback.message.edit_text(text=variants[curr_var - 1], reply_markup=double_inline_kb)
    logger.info("Пользователь нажал стрелку влево.")
    await callback.answer()


@router.callback_query(RewrittenCallbackFactory.filter(F.next_move == 5), StateFilter(FSMRewrite.rewrote))
async def process_right_variant(callback: CallbackQuery, state: FSMContext):
    variants = (await state.get_data())["answers"]
    curr_var = (await state.get_data())["variant"]
    await state.update_data({"variant": curr_var + 1})
    if curr_var + 2 == len(variants):
        await callback.message.edit_text(text=variants[curr_var + 1], reply_markup=left_inline_kb)
    else:
        await callback.message.edit_text(text=variants[curr_var + 1], reply_markup=double_inline_kb)
    logger.info("Пользователь нажал стрелку вправо.")
    await callback.answer()


@router.callback_query(RewrittenCallbackFactory.filter(F.next_move == 0), StateFilter(FSMRewrite.rewrote))
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(None)
    await state.clear()
    await callback.message.answer(text=LEXICON["greeting"], reply_markup=keyboard)
    await callback.answer()
    logger.info("Пользователь вышел из рерайтинга.")
