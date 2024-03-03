from aiogram.utils.keyboard import InlineKeyboardBuilder


async def add_childs_in_basket():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="1-му ребенку", callback_data="first_child_add_basket")
    keyboard.button(text="2-му ребенку", callback_data="second_child_add_basket")
    keyboard.button(text="3-му ребенку", callback_data="third_child_add_basket")
    keyboard.button(text="4-му ребенку", callback_data="four_child_add_basket")
    keyboard.button(text="назад \U000023EA", callback_data="who_will_order")
    keyboard.adjust(2)

    return keyboard.as_markup()


async def childs_in_basket():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад \U000023EA", callback_data="who_will_order")
    keyboard.adjust(2)
    return keyboard.as_markup()
