from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту

@dataclass
class GigaBot:
    key: str


@dataclass
class Config:
    tg_bot: TgBot
    giga: GigaBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), giga=GigaBot(key=env("AUTH_KEY")))
