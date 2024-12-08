import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config_data.config import config

logger = logging.getLogger(__name__)


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user: User = data.get('event_from_user')
        if user is not None:
            if int(user.id) == int(config.tg_bot.admin_id):
                data["user"] = "admin"
            else:
                data["user"] = "user"
        logger.info("Отработала миддлварь на админа.")
        return await handler(event, data)
