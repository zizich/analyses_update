from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import date_person_db, date_add_db


async def gth_after_add_date(kb, date_found):
    kb.button(text="удалить дату \U00002702\U0000FE0F\U0001F564",
              callback_data=f"delAddDate{date_found}")
    kb.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
    kb.adjust(1)
    return kb.as_markup()
