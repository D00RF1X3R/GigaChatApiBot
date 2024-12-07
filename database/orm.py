import asyncio
import logging

from sqlalchemy import select

from database.database import async_session_factory as sf, engine, Base
from database.models import UsersOrm, RewritesOrm, MediaOrm

logger = logging.getLogger(__name__)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Таблицы созданы успешно.")


async def insert_data(user_id, username):
    user = UsersOrm(id=user_id, username=username, banned=False, admin=False)
    async with sf() as session:
        session.add(user)
        await session.commit()
    logging.info("Пользователь записан.")


async def check_user(user_id):
    async with sf() as session:
        query = select(UsersOrm).where(UsersOrm.id == user_id)
        try:
            (await session.execute(query)).scalars().all()[0].id
        except IndexError:
            logging.info("Пользователя нет в базе.")
            return False
        logging.info("Пользователь есть в базе.")
        return True


async def select_user(user_id):
    async with sf() as session:
        query = select(UsersOrm).where(UsersOrm.id == user_id)
        res = await session.execute(query)
        user = res.scalars().all()[0]
        logging.info("Пользователь найден")
        return user


async def insert_rewritten_text(user_id, text):
    async with sf() as session:
        text_to_insert = RewritesOrm(owner=user_id, text=text)
        session.add(text_to_insert)
        logging.info("Текст сохранен.")
        await session.commit()


async def add_media_to_db(name, file_id):
    async with sf() as session:
        file = MediaOrm(name=name, file_id=file_id)
        session.add(file)
        logging.info("Файл добавлен.")
        await session.commit()


async def get_media_id_from_bd(name):
    async with sf() as session:
        query = select(MediaOrm).where(MediaOrm.name == name)
        res = await session.execute(query)
        file_id = res.scalars().all()[0]
        logging.info("ID файла получен.")
        return file_id.file_id
