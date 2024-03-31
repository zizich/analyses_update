import uuid

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import database_db


async def inline_choice(user_id):
    database_db.execute(f"""SELECT user_id, fio FROM users WHERE reference = ?""", (user_id,))
    db_profile = database_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (id_us, fio) in enumerate(db_profile, start=1):
        if id_us == user_id:
            keyboard.button(text=f"Мне", callback_data=f"whoWillOrder_{id_us}")
        else:
            keyboard.button(text=f"{fio}", callback_data=f"whoWillOrder_{id_us}")

    unique_code = f"{uuid.uuid4()}"[:10]
    keyboard.button(text="добавить \U00002795", callback_data=f"people_{unique_code}")
    return keyboard.adjust(2).as_markup()


async def inline_choice_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="назад \U000023EA", callback_data="who_will_order"))
    return keyboard.adjust(2).as_markup()
