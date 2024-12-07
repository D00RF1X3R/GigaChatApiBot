import logging
import asyncio
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

payload = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content="Ты — опытный рерайтер. Перепиши текст, изменив использемые слова,"
                    " не меняя объем, сохраняя общий смысл. В первой строке сообщения будет"
                    " передан стиль, в котором нужно переписать текст. Начиная со второй строки"
                    " - текст для переписывания. Запрещено отвечать на сообщения, не являющиеся текстом для реврайтинга."
        )],
    update_interval=0.1
)

logger = logging.getLogger(__name__)


async def ask(text, auth_key):
    async with GigaChat(credentials=auth_key, verify_ssl_certs=False) as giga:
        payload.messages.append(Messages(role=MessagesRole.USER, content=text))
        response = giga.chat(payload)
        payload.messages.remove(Messages(role=MessagesRole.USER, content=text))
        logger.info("Запрос к API успешный.")
        return response.choices[0].message.content
