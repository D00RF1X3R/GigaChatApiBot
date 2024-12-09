from aiogram.types import FSInputFile
from os import listdir

from config_data.config import config


async def load_files(bot):  # Загрузка файлов аватарок автора
    files = listdir("media/files")
    fin = []
    for i in files:
        file = FSInputFile(f"media/files/{i}")
        file_id = await bot.send_photo(chat_id=config.tg_bot.admin_id, photo=file)
        fin_id = file_id.photo[0].file_id
        fin.append({i: fin_id})
    return fin
