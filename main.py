import asyncio

from aiogram_dialog import setup_dialogs
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import rewrite, starter

from database.orm import insert_data, create_tables, add_media_to_db
from config_data.config import config

from dialog import authordialog

from media.medialodaer import load_files


# Функция конфигурирования и запуска бота
async def main():
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    dp["giga_key"] = config.giga.key

    await create_tables()

    res = await load_files(bot)
    for i in res:
        await add_media_to_db(list(i.keys())[0], i[list(i.keys())[0]])

    dp.include_router(starter.router)
    dp.include_router(rewrite.router)

    dp.include_router(authordialog.author_tab)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
