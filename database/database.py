import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config_data.config import config


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=config.db.url(),
    echo=True,
)

async_session_factory = async_sessionmaker(engine)
