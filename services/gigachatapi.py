import asyncio
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from config_data.config import Config, load_config

config: Config = load_config()
auth_key = config.giga.key

payload = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content="Ты — опытный копирайтер. Перепиши текст, изменив использемые слова,"
                    " не меняя объем, сохраняя общий смысл. В первой строке сообщения будет"
                    " передан стиль, в котором нужно переписать текст. Начиная со второй строки"
                    " - текст для переписывания."
        )],
    update_interval=0.1
)


async def ask(text):
    async with GigaChat(credentials=auth_key, verify_ssl_certs=False) as giga:
        payload.messages.append(Messages(role=MessagesRole.USER, content=text))
        response = giga.chat(payload)
        payload.messages.remove(Messages(role=MessagesRole.USER, content=text))
        return response.choices[0].message.content
