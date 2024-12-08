from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    prov_token: str
    admin_id: int


@dataclass
class GigaBot:
    key: str


@dataclass
class DataBase:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    def url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class Config:
    tg_bot: TgBot
    giga: GigaBot
    db: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), prov_token=env('PROVIDER_TOKEN'), admin_id=env('ADMIN_ID')),
                  giga=GigaBot(key=env("AUTH_KEY")),
                  db=DataBase(env("DB_HOST"), env("DB_PORT"), env("DB_USER"), env("DB_PASS"), env("DB_NAME")))


config: Config = load_config()
