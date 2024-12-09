from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    prov_token: str  # Токен для донатов
    admin_id: int  # ID админа


@dataclass
class GigaBot:
    key: str  # Ключ авторизации бота


@dataclass
class DataBase:
    DB_HOST: str  # Хост БД
    DB_PORT: int  # Порт БД, искать в документации конкретной БД
    DB_USER: str  # Имя пользователя БД
    DB_PASS: str  # Пароль пользователя
    DB_NAME: str  # Название БД

    def url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class Config:
    tg_bot: TgBot
    giga: GigaBot
    db: DataBase


def load_config(path: str | None = None) -> Config:  # Функция загрузки пользователя
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), prov_token=env('PROVIDER_TOKEN'), admin_id=env('ADMIN_ID')),
                  giga=GigaBot(key=env("AUTH_KEY")),
                  db=DataBase(env("DB_HOST"), env("DB_PORT"), env("DB_USER"), env("DB_PASS"), env("DB_NAME")))


config: Config = load_config()
