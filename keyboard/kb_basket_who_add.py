from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_choice():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Мне \U0001F64B", callback_data="my_order_button"))
    keyboard.add(InlineKeyboardButton(text="Другим \U0001F465", callback_data="others_order_button"))
    keyboard.add(InlineKeyboardButton(text="назад \U000023EA", callback_data="back_to_basket_menu"))
    return keyboard.adjust(2).as_markup()


async def inline_choice_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="назад \U000023EA", callback_data="who_will_order"))
    return keyboard.adjust(2).as_markup()
