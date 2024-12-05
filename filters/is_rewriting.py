from database.user_db import user_data
from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsRewriting(BaseFilter):
    async def __call__(self, message: Message):
        return user_data[message.from_user.id]["rewriting"]
