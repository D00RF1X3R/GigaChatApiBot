import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config_data.config import config

from database.orm import check_user_ban

logger = logging.getLogger(__name__)


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user: User = data.get('event_from_user')
        logger.info("Отработала миддлварь на забаненных пользователей.")
        if user is not None:
            if not await check_user_ban(user.id):
                return await handler(event, data)
            else:
                logger.info("Не пропустил пользователя в бане.")
                return
