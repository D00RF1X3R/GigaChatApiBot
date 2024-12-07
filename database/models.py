from sqlalchemy import Table, Column, Integer, String, BOOLEAN, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    admin: Mapped[bool | None]
    banned: Mapped[bool]


class RewritesOrm(Base):
    __tablename__ = "rewrites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[str] = relationship(UsersOrm, cascade="all, delete", backref="children")


class MediaOrm(Base):
    __tablename__ = "media"

    name: Mapped[str] = mapped_column(primary_key=True)
    file_id: Mapped[str]
