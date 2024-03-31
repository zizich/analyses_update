from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import database_db


async def kb_patterns():

    database_db.execute(f"""SELECT * FROM users_pattern""")
    keyboard = InlineKeyboardBuilder()

    for i, (usr_id, name, analysis) in enumerate(database_db.fetchall(), start=1):
        keyboard.button(text=f"{i}. {name}", callback_data=f"pat_{name}")

    keyboard.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
    keyboard.adjust(1)

    return keyboard.as_markup()


