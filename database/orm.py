import asyncio

from sqlalchemy import select

from database.database import async_session_factory as sf, engine, Base
from database.models import UsersOrm, RewritesOrm


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data(user_id):
    user = UsersOrm(id=user_id, rewriting=False)
    async with sf() as session:
        session.add(user)
        await session.commit()


async def select_user(user_id):
    async with sf() as session:
        query = select(UsersOrm).where(UsersOrm.id == user_id)
        res = await session.execute(query)
        user = res.scalars().all()[0]
        return user


async def change_rewriting(user_id):
    async with sf() as session:
        user = await session.get(UsersOrm, user_id)
        user.rewriting = not user.rewriting
        await session.commit()


async def insert_rewritten_text(user_id, text):
    async with sf() as session:
        text_to_insert = RewritesOrm(owner=user_id, text=text)
        session.add(text_to_insert)
        await session.commit()
