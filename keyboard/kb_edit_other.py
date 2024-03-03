from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import job_db


async def edit_people_one():
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

    return keyboard.as_markup()


async def back_to_edit_people():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")

    return keyboard.adjust(1).as_markup()


async def choice_city():
    keyboard = InlineKeyboardBuilder()

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityOtherAdd_{city}")
    keyboard.adjust(1)

    return keyboard.as_markup()
