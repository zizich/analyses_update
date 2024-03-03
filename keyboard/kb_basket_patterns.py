from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import pattern_db


async def kb_patterns(user_id):

    pattern_db.execute(f"""SELECT * FROM user_{user_id}""")
    keyboard = InlineKeyboardBuilder()

    for i, (date, name, analysis) in enumerate(pattern_db.fetchall(), start=1):
        keyboard.button(text=f"{i}. {name}", callback_data=f"pat_{date}")

    keyboard.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
    keyboard.adjust(1)

    return keyboard.as_markup()


