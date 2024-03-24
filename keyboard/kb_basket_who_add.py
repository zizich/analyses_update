from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.base import cursor_db


async def inline_choice(user_id):
    cursor_db.execute(f"""SELECT user_id, fio FROM users_{user_id}""")
    db_profile = cursor_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (id_us, fio) in enumerate(db_profile, start=1):
        if id_us == f"{user_id}-1":
            keyboard.button(text=f"Мне", callback_data=f"whoWillOrder_{id_us}")
        else:
            keyboard.button(text=f"{fio}", callback_data=f"whoWillOrder_{id_us}")

    return keyboard.adjust(2).as_markup()


async def inline_choice_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="назад \U000023EA", callback_data="who_will_order"))
    return keyboard.adjust(2).as_markup()
