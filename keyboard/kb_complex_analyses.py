from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import database_db, connect_database


async def kb_complex():
    keyboard = InlineKeyboardBuilder()

    all_complex_out = database_db.execute("""SELECT * FROM analyses_complex""").fetchall()

    for i, (name_complex, code_complex, code_analyses) in enumerate(all_complex_out, start=1):
        keyboard.button(text=name_complex, callback_data=f"grp_{code_complex}")

    keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
    keyboard.adjust(2)

    return keyboard.as_markup()

