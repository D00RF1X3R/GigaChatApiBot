import logging

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON

from keyboards.starter import admin_kb
from keyboards.admin import AdminCallbackFactory, build_kb, admin_tab_kb

from states.admin import FSMAdmin

from database.orm import get_users, user_state, get_counts

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(AdminCallbackFactory.filter(F.next_move == 0), StateFilter(FSMAdmin.admin))
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(None)
    await state.clear()
    await callback.message.answer(text=LEXICON["admin_greet"], reply_markup=admin_kb)
    await callback.answer()
    logger.info("Пользователь вышел из истории переписей.")


@router.callback_query(AdminCallbackFactory.filter(F.next_move == 0), StateFilter(FSMAdmin.banned_users))
@router.callback_query(AdminCallbackFactory.filter(F.next_move == 0), StateFilter(FSMAdmin.users))
async def process_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMAdmin.admin)
    await callback.message.edit_text(text=LEXICON["admin_greet"], reply_markup=admin_tab_kb)


@router.callback_query(AdminCallbackFactory.filter(~F.next_move), StateFilter(FSMAdmin.users))
async def ban_user(callback: CallbackQuery, callback_data: AdminCallbackFactory, state: FSMContext):
    await user_state(callback_data.id, ban=True)
    res = await get_users()
    if res:
        await callback.message.edit_text(text='Все пользователи:', reply_markup=build_kb(res))
    else:
        await state.set_state(FSMAdmin.admin)
        await callback.message.edit_text(text='Пользователи закончились.', reply_markup=admin_tab_kb)
    logger.info("Пользователь разблокирован")
    await callback.answer("Пользователь разблокирован")


@router.callback_query(AdminCallbackFactory.filter(~F.next_move), StateFilter(FSMAdmin.banned_users))
async def unban_user(callback: CallbackQuery, callback_data: AdminCallbackFactory, state: FSMContext):
    await user_state(callback_data.id)
    res = await get_users(banned=True)
    if res:
        await callback.message.edit_text(text='Забаненные пользователи:', reply_markup=build_kb(res))
    else:
        await state.set_state(FSMAdmin.admin)
        await callback.message.edit_text(text='Забаненные пользователи закончились.', reply_markup=admin_tab_kb)
    logger.info("Пользователь заблокирован")
    await callback.answer("Пользователь заблокирован")


@router.callback_query(AdminCallbackFactory.filter(F.next_move == 1), StateFilter(FSMAdmin.admin))
async def process_ban_users(callback: CallbackQuery, callback_data: AdminCallbackFactory, state: FSMContext):
    res = await get_users()
    if res:
        await state.set_state(FSMAdmin.users)
        await callback.message.edit_text(text='Все пользователи:', reply_markup=build_kb(res))
        await callback.answer()
    else:
        await callback.answer("Нет пользователей.")


@router.callback_query(AdminCallbackFactory.filter(F.next_move == 2), StateFilter(FSMAdmin.admin))
async def process_unban_users(callback: CallbackQuery, callback_data: AdminCallbackFactory, state: FSMContext):
    res = await get_users(banned=True)
    if res:
        await state.set_state(FSMAdmin.banned_users)
        await callback.message.edit_text(text='Забаненные пользователи:', reply_markup=build_kb(res))
        await callback.answer()
    else:
        await callback.answer("Нет забаненных пользователей.")


@router.callback_query(AdminCallbackFactory.filter(F.next_move == 3), StateFilter(FSMAdmin.admin))
async def process_counters(callback: CallbackQuery, state: FSMContext):
    res = await get_counts()
    await callback.answer(f"Количество пользователей: {res[0]}\n"
                          f"Количество переписей: {res[1]}")
