from aiogram.utils.keyboard import InlineKeyboardBuilder


def edit_people_one():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Имя ➡️ ", callback_data="people_name_one")
    keyboard.button(text="Фамилия ➡️️", callback_data="people_female_one")
    keyboard.button(text="Отчество ➡️", callback_data="people_patronymic_one")
    keyboard.button(text="Дата рождения ➡️", callback_data="people_birth_day_one")
    keyboard.button(text="Телефон ➡️ ", callback_data="people_phone_one")
    keyboard.button(text="e-mail ➡️ ", callback_data="people_email_one")
    keyboard.button(text="Город ➡️", callback_data="city_people_one")
    keyboard.button(text="Адрес ➡️", callback_data="people_adress_one")
    keyboard.adjust(2)

    return keyboard
