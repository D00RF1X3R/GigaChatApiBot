import asyncio


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import rewrite, starter

from database.orm import insert_data, create_tables
from config_data.config import config


# Функция конфигурирования и запуска бота
async def main():

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    dp["giga_key"] = config.giga.key

    await create_tables()

    dp.include_router(starter.router)
    dp.include_router(rewrite.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
