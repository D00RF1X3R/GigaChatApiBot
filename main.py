import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import rewrite, starter


# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config()
    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(starter.router)
    dp.include_router(rewrite.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
