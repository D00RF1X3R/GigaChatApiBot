import operator

from aiogram.enums.content_type import ContentType
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from magic_filter import F

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Radio, Row, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from states.authortab import FSMAuthor, FSMContext

from database.orm import get_media_id_from_bd

from lexicon.lexicon import LEXICON

from keyboards.starter import keyboard, next_kb


async def on_click(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await callback.message.answer(text=LEXICON['leave_author'], reply_markup=next_kb)


async def get_social(dialog_manager: DialogManager, **kwargs):
    socials = [
        ("Telegram", '1'),
        ("VK", '2'),
        ("GitHub", '3')
    ]
    res = dialog_manager.find("r_socials").get_checked()
    if res == '1':
        image_id = await get_media_id_from_bd("tg.gif")
        image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
        return {
            "socials": socials,
            "count": len(socials),
            "curr_social": "Telegram",
            "media": image,
            "add_media": True,
            "tg": True,
            "vk": False,
            "gh": False,
        }
    elif res == '2':
        image_id = await get_media_id_from_bd("vk.jpg")
        image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
        return {
            "socials": socials,
            "count": len(socials),
            "curr_social": "VK",
            "media": image,
            "add_media": True,
            "tg": False,
            "vk": True,
            "gh": False,
        }
    elif res == '3':
        image_id = await get_media_id_from_bd("gh.jpg")
        image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
        return {
            "socials": socials,
            "count": len(socials),
            "curr_social": "GitHub",
            "media": image,
            "add_media": True,
            "tg": False,
            "vk": False,
            "gh": True,
        }
    return {
        "curr_social": "нету",
        "socials": socials,
        "count": len(socials),
        "add_media": False,
    }


socials_kbd = Radio(
    Format("🔴 {item[0]}"),
    Format("⚪ {item[0]}"),
    id="r_socials",
    item_id_getter=operator.itemgetter(1),
    items="socials",
)

text = Format(
    "Я - создатель бота, больше о моих соцсетях можно узнать ниже, нажав на чекбокс! \n\n"
)

author_tab = Dialog(
    Window(
        text,
        Const(
            "Мой личный телеграм, можно писать по поводу ошибок:\n https://t.me/d00r_f1x3r",
            when="tg"
        ),
        Const(
            "Мой личный вк, писать сюда не стоит.\n https://vk.com/iheaaywdily",
            when="vk"
        ),
        Const(
            "Мой GitHub, на который я пока выкладываю только учебные проекты:\n https://github.com/D00RF1X3R",
            when="gh"
        ),
        Row(
            socials_kbd,
            Button(text=Const("⬅️"), id="cancel", on_click=on_click)
        ),
        DynamicMedia(
            "media",
            when='add_media',
        ),
        getter=get_social,
        state=FSMAuthor.in_author_tab
    )
)
