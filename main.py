import asyncio
import logging

from aiogram_dialog import setup_dialogs
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import rewrite, starter, prererwrite

from database.orm import insert_data, create_tables, add_media_to_db
from config_data.config import config

from dialog import authordialog

from media.medialodaer import load_files


# Функция конфигурирования и запуска бота
async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
               '%(lineno)d - %(name)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Логгер запущен!")

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    dp["giga_key"] = config.giga.key
    dp["prov_token"] = config.tg_bot.prov_token

    ans = input("Хотите ли вы создать новые таблицы?\n 1 - да, 2 - нет \n?: ")
    if ans == '1':
        await create_tables()
        logger.info("Таблицы сделаны.")

        res = await load_files(bot)
        for i in res:
            await add_media_to_db(list(i.keys())[0], i[list(i.keys())[0]])
        logger.info("Медиа собраны.")

    dp.include_router(starter.router)
    dp.include_router(rewrite.router)
    dp.include_router(prererwrite.router)

    dp.include_router(authordialog.author_tab)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
