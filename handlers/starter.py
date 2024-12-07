import logging

import uuid

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PreCheckoutQuery, ContentType, SuccessfulPayment

from aiogram_dialog import DialogManager

from states.rewriting import FSMRewrite
from states.authortab import FSMAuthor

from lexicon.lexicon import LEXICON
from keyboards.starter import keyboard

from database.orm import insert_data, check_user

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    if await check_user(message.from_user.id):
        logger.info(f"Пользователь {message.from_user.username} уже есть в базе.")
    else:
        await insert_data(message.from_user.id, message.from_user.username)
        logger.info(f"Пользователь {message.from_user.id} создан.")
    await message.answer(text=LEXICON['/start'], reply_markup=keyboard)


@router.message(lambda message: message.text == "Помощь", StateFilter(default_state))
async def process_help(message: Message):
    logger.info("Помощь оказана")
    await message.answer(text=LEXICON["help"], reply_markup=keyboard)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    logger.info("Помощь оказана")
    await message.answer(text=LEXICON["help"], reply_markup=keyboard)


@router.message(lambda message: message.text == "Автор", StateFilter(default_state))
async def process_author(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await state.set_state(FSMAuthor.in_author_tab)
    await dialog_manager.start(FSMAuthor.in_author_tab)
    logger.info("Переход к авторам")


@router.message(StateFilter(FSMAuthor.in_author_tab))
async def leave_author(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON['greeting'], reply_markup=keyboard)
    logger.info("Уход от авторов")


@router.message(lambda message: message.text == "Начать рерайтинг", StateFilter(default_state))
async def rewrite(message: Message, state: FSMContext):
    await state.set_state(FSMRewrite.rewriting)
    await message.answer(text="Поехали!")
    logger.info("Начало рерайта")


@router.message(lambda message: message.text == "Дать денег", StateFilter(default_state))
async def create_invoice(message: Message, prov_token):
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
async def process_pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment_handler(message: Message):
    await message.answer(text="Спасибо за донат!!!")
