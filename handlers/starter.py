import logging

import uuid

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PreCheckoutQuery, ContentType

from aiogram_dialog import DialogManager

from states.rewriting import FSMRewrite
from states.authortab import FSMAuthor
from states.admin import FSMAdmin

from lexicon.lexicon import LEXICON
from keyboards.starter import keyboard, admin_kb
from keyboards.prerewritekb import pre_rewrite_kb
from keyboards.admin import admin_tab_kb

from database.orm import insert_data, check_user, make_admin

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, user):  # Обработка команды /start
    if await check_user(message.from_user.id):
        logger.info(f"Пользователь {message.from_user.username} уже есть в базе.")
        if user == "admin":
            await make_admin(message.from_user.id)
            await message.answer(text=LEXICON['/start'] + "\nВы админ!!!", reply_markup=admin_kb)
        else:
            await message.answer(text=LEXICON['/start'], reply_markup=keyboard)
    else:
        await insert_data(message.from_user.id, message.from_user.username)
        logger.info(f"Пользователь {message.from_user.id} создан.")
        await message.answer(text=LEXICON['/start'], reply_markup=keyboard)


@router.message(lambda message: message.text == "Админка", StateFilter(default_state))
async def process_admin(message: Message, user, state: FSMContext):  # Переход в админку
    if user == "admin":
        await state.set_state(FSMAdmin.admin)
        await message.answer(text=LEXICON["admin_greet"], reply_markup=admin_tab_kb)


@router.message(lambda message: message.text == "Помощь", StateFilter(default_state))
async def process_help(message: Message):  # Переход в помощь
    logger.info("Помощь оказана")
    await message.answer(text=LEXICON["help"], reply_markup=keyboard)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):  # Переход в помощь
    logger.info("Помощь оказана")
    await message.answer(text=LEXICON["help"], reply_markup=keyboard)


@router.message(lambda message: message.text == "Автор", StateFilter(default_state))
async def process_author(message: Message, state: FSMContext,
                         dialog_manager: DialogManager):  # Переход в страницы автора
    await state.set_state(FSMAuthor.in_author_tab)
    await dialog_manager.start(FSMAuthor.in_author_tab)
    logger.info("Переход к авторам")


@router.message(StateFilter(FSMAuthor.in_author_tab))
async def leave_author(message: Message, state: FSMContext, user):  # Выход из страницы автора
    await state.clear()
    if user == "admin":
        await message.answer(text=LEXICON["admin_greet"], reply_markup=admin_kb)
    else:
        await message.answer(text=LEXICON["greeting"], reply_markup=keyboard)
    logger.info("Уход от авторов")


@router.message(lambda message: message.text == "Начать рерайтинг", StateFilter(default_state))
async def rewrite(message: Message, state: FSMContext):  # Переход в страницу рерайтинга
    await state.set_state(FSMRewrite.pre_rewrite)
    await message.answer(text=LEXICON['split'], reply_markup=pre_rewrite_kb)
    logger.info("Начало рерайта")


@router.message(lambda message: message.text == "Дать денег", StateFilter(default_state))
async def create_invoice(message: Message, prov_token):  # Дать ссылку на донат
    payment_id = str(uuid.uuid4())
    await message.answer_invoice(
        title='Дать денег автору.',
        description='Эти деньги нужны не так самому автору, как создателям GigaChat, чтобы сделать более умного бота.',
        payload=payment_id,
        provider_token=prov_token,
        currency='RUB',
        prices=[
            types.LabeledPrice(label='Оплата услуг', amount=2281)
        ]
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery):  # Что-то нужное для донатов
    await query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment_handler(message: Message):  # Обработка успешной оплаты
    await message.answer(text="Спасибо за донат!!!")
