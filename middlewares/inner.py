import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class BadRequestMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        pass
