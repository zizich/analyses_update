from aiogram.utils.keyboard import InlineKeyboardBuilder


def buttons_edit_childs_one():
    keyboard = InlineKeyboardBuilder()
    keyboard.button("Имя ➡️ ", callback_data="name_one")
    keyboard.button("Фамилия ➡️️", callback_data="female_one")
    keyboard.button("Отчество ➡️", callback_data="patronymic_one")
    keyboard.button("Дата рождения ➡️", callback_data="birth_day_one")
    keyboard.adjust(1)

    return keyboard


def buttons_edit_childs_two():
    keyboard = InlineKeyboardBuilder()
    keyboard.button("Имя ➡️ ", callback_data="name_two")
    keyboard.button("Фамилия ➡️️", callback_data="female_two")
    keyboard.button("Отчество ➡️", callback_data="patronymic_two")
    keyboard.button("Дата рождения ➡️", callback_data="birth_day_two")
    keyboard.adjust(1)

    return keyboard


def buttons_edit_childs_three():
    keyboard = InlineKeyboardBuilder()
    keyboard.button("Имя ➡️ ", callback_data="name_three")
    keyboard.button("Фамилия ➡️️", callback_data="female_three")
    keyboard.button("Отчество ➡️", callback_data="patronymic_three")
    keyboard.button("Дата рождения ➡️", callback_data="birth_day_three")
    keyboard.adjust(1)

    return keyboard


def buttons_edit_childs_four():
    keyboard = InlineKeyboardBuilder()
    keyboard.button("Имя ➡️ ", callback_data="name_four")
    keyboard.button("Фамилия ➡️️", callback_data="female_four")
    keyboard.button("Отчество ➡️", callback_data="patronymic_four")
    keyboard.button("Дата рождения ➡️", callback_data="birth_day_four")
    keyboard.adjust(1)

    return keyboard
