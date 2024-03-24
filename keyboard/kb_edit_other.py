from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.base import job_db


async def edit_people(user_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="ФИО ➡️ ", callback_data=f"peopleName_{user_id}")
    keyboard.button(text="Дата рождения ➡️", callback_data=f"peopleBirth_{user_id}")
    keyboard.button(text="Телефон ➡️ ", callback_data=f"peoplePhone_{user_id}")
    keyboard.button(text="e-mail ➡️ ", callback_data=f"peopleEmail_{user_id}")
    keyboard.button(text="Город ➡️", callback_data=f"cityPeople_{user_id}")
    keyboard.button(text="Адрес ➡️", callback_data=f"peopleAdress_{user_id}")
    keyboard.button(text="назад", callback_data=f"others_{user_id}")
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


async def choice_edit_city():
    keyboard = InlineKeyboardBuilder()

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityEdit_{city}")
    keyboard.adjust(1)

    return keyboard.as_markup()
