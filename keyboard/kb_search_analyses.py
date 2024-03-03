from aiogram.utils.keyboard import InlineKeyboardBuilder


async def base_menu_analyses():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Комплексы \U0001F9EA", callback_data="group_buttons")
    keyboard.button(text="Поиск \U0001F50E", callback_data="search_analysis")
    keyboard.button(text="Стоп лист \u26D4\ufe0f", callback_data="stop_list")
    keyboard.adjust(1)

    return keyboard.as_markup()


async def info_by_analyses(id_analyses):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="добавить \U00002705", callback_data=f"addAn_{id_analyses}")
    keyboard.button(text="информация \U00002753", callback_data=f"infoAn_{id_analyses}")
    keyboard.button(text="поиск \U0001F50E", callback_data="search_analysis")
    keyboard.button(text="удалить \U0000274E", callback_data=f"delAn_{id_analyses}")
    keyboard.button(text="назад \U000023EA", callback_data="back_to_previous_search")
    keyboard.adjust(2)

    return keyboard.as_markup()


async def kb_previous_search():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="поиск \U0001F50E", callback_data="search_analysis")
    keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
    keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")

    return keyboard.adjust(1).as_markup()


async def kb_search_analyses_after_done(kb):
    kb.button(text="поиск \U0001F50E", callback_data="search_analysis")
    kb.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
    kb.button(text="назад \U000023EA", callback_data="back_to_analyses")
    kb.adjust(1).as_markup()

    return kb
