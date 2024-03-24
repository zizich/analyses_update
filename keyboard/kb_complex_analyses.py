from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.base import complex_analyses_db


async def kb_complex():
    keyboard = InlineKeyboardBuilder()

    all_complex_out = complex_analyses_db.execute("""SELECT * FROM complex""").fetchall()

    for i, (name_rus, name_eng, numbers) in enumerate(all_complex_out, start=1):
        keyboard.button(text=f"{name_rus}", callback_data=f"group_{name_eng}")

    keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
    keyboard.adjust(2)

    return keyboard.as_markup()

