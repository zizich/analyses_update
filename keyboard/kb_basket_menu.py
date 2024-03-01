from aiogram.utils.keyboard import InlineKeyboardBuilder


def basket_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="1. Анализы \U0001F52C", callback_data="back_to_analyses")
    keyboard.button(text="4. Кому заказать? \U0001F465", callback_data="who_will_order")
    keyboard.button(text="2. Шаблоны \u2B50", callback_data="pattern")
    keyboard.button(text="5. Выбрать дату \U0001F4C6", callback_data="exit_or_self_conversion")
    keyboard.button(text="3. Изм. список \U0001F9EA", callback_data="edit_list_order")
    keyboard.button(text="6. Комментарии \U0001F4AC", callback_data="comment")
    keyboard.button(text="7. Подтвердить заявку \u2705", callback_data="confirm_the_order")
    keyboard.adjust(2)

    return keyboard
