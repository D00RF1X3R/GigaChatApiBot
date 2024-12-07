from sqlalchemy import Table, Column, Integer, String, BOOLEAN, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    rewriting: Mapped[bool | None]


class RewritesOrm(Base):
    __tablename__ = "rewrites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))
