from aiogram.utils.keyboard import InlineKeyboardBuilder


async def delivery_in_basket():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="\U0001F3E0 вызов на дом", callback_data="go_to_home")
    keyboard.button(text="\U0001F3C3 самообращение", callback_data="go_to_medical")
    keyboard.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
    keyboard.adjust(1)

    return keyboard.as_markup()
