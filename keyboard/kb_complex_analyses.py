from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import database_db, connect_database


async def kb_complex():
    keyboard = InlineKeyboardBuilder()

    all_complex_out = database_db.execute("""SELECT complex FROM analyses""").fetchall()

    collection_complex = []
    for i, (commplex) in enumerate(all_complex_out, start=1):
        collection_complex.append(commplex)

    unique_complex = list(set(collection_complex))

    for unique in unique_complex:
        keyboard.button(text=f"{unique}", callback_data=f"grp_{unique}")

    keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
    keyboard.adjust(2)

    return keyboard.as_markup()

