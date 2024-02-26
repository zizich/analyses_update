from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import cursor_db
from keyboard import reply_menu

router = Router(name=__name__)


@router.message(F.text.in_(["\U0001F476 Дети"]))
async def process_profile_child(message: Message):
    user_id = message.from_user.id
    keyboard_four_child = InlineKeyboardBuilder()
    try:
        city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

        cursor_db.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,))
        db_profile = cursor_db.fetchall()

        phone = db_profile[0][5]
        email = db_profile[0][6]
        home_address = db_profile[0][7]
        child_name = db_profile[0][11]
        child_female = db_profile[0][12]
        child_patronymic = db_profile[0][13]
        child_birth_date = db_profile[0][14]
        two_child_name = db_profile[0][18]
        two_child_female = db_profile[0][19]
        two_child_patronymic = db_profile[0][20]
        two_child_birth_date = db_profile[0][21]
        three_child_name = db_profile[0][25]
        three_child_female = db_profile[0][26]
        three_child_patronymic = db_profile[0][27]
        three_child_birth_date = db_profile[0][28]
        four_child_name = db_profile[0][32]
        four_child_female = db_profile[0][33]
        four_child_patronymic = db_profile[0][34]
        four_child_birth_date = db_profile[0][35]

        if child_name is None and two_child_name is None and three_child_name is None and four_child_name is None:
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="добавить 1-го \U0001F476  ️➡️", callback_data="add_child_button")

            await message.answer(text="Данных о наличии детей - нет", reply_markup=keyboard.as_markup())

        if child_name is not None and two_child_name is None and three_child_name is None and four_child_name is None:
            keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
            keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
            keyboard_four_child.button(text="добавить 2-го \U0001F476  ️➡️", callback_data="add_two_child_button")
            keyboard_four_child.adjust(2)
            await message.answer(text="<b>\U0001F476 Дети:</b>" + "\n" +
                                      f"     ♻️ Город: <b>{city}</b>" + "\n" +
                                      f"     ♻️ Адресс: <b>{home_address}</b>" + "\n" +
                                      f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                      f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                      f" 1️⃣  ♻️ Имя:   <b>{child_name}</b>" + "\n" +
                                      f"     ♻️ Фамилия: <b>{child_female}</b>" + "\n" +
                                      f"     ♻️ Отчество: <b>{child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{child_birth_date}</b>",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard_four_child.as_markup())
        if two_child_name is not None and three_child_name is None and four_child_name is None:
            if child_name == "NULL":
                keyboard_four_child.button(text="добавить 1-го \U0001F476  ️➡️", callback_data="add_child_button")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="редактировать 2-го \U0001F476", callback_data="edit_second_child")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="добавить 3-го \U0001F476  ️➡️", callback_data="add_three_child_button")
                keyboard_four_child.adjust(2)
            elif two_child_name == "NULL":
                keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="добавить 2-го \U0001F476  ️➡️", callback_data="add_two_child_button")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="добавить 3-го \U0001F476  ️➡️", callback_data="add_three_child_button")
                keyboard_four_child.adjust(2)
            else:
                keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="редактировать 2-го \U0001F476", callback_data="edit_second_child")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="добавить 3-го \U0001F476  ️➡️", callback_data="add_three_child_button")
                keyboard_four_child.adjust(2)

            await message.answer(text="<b>\U0001F476 Дети:</b>" + "\n" +
                                      f"     ♻️ Город: <b>{city}</b>" + "\n" +
                                      f"     ♻️ Адресс: <b>{home_address}</b>" + "\n" +
                                      f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                      f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                      f" 1️⃣  ♻️ ФИО: <b>{child_name}</b> <b>{child_female}</b> <b>{child_patronymic}</b>"
                                      + "\n" +
                                      f"     ♻️ Дата рождения: <b>{child_birth_date}</b>" + "\n" +
                                      f" 2️⃣  ♻️ ФИО: <b>{two_child_name}</b> <b>{two_child_female}</b> "
                                      f"<b>{two_child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{two_child_birth_date}</b>",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard_four_child.as_markup())
        # при условии если 3-й ребенок не пустой, а 4-й пустой, то выводим на консоль все 3-х детей
        if three_child_name is not None and four_child_name is None:
            # Если удален 1-й ребенок, то добавляем кнопку - добавить 1-го ребенка
            if child_name == "NULL":
                keyboard_four_child.button(text="добавить 1-го \U0001F476  ️➡️", callback_data="add_child_button")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="редактировать 2-го \U0001F476", callback_data="edit_second_child")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="редактировать 3-го \U0001F476", callback_data="edit_three_child")
                keyboard_four_child.button(text="удалить 3-го \U0001F476", callback_data="delete_child_three")
                keyboard_four_child.button(text="добавить 4-го \U0001F476  ️➡️", callback_data="add_four_child_button")
                keyboard_four_child.adjust(2)
            elif two_child_name == "NULL":
                keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="добавить 2-го \U0001F476  ️➡️", callback_data="add_two_child_button")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="редактировать 3-го \U0001F476", callback_data="edit_three_child")
                keyboard_four_child.button(text="удалить 3-го \U0001F476", callback_data="delete_child_three")
                keyboard_four_child.button(text="добавить 4-го \U0001F476  ️➡️", callback_data="add_four_child_button")
                keyboard_four_child.adjust(2)

            elif three_child_name == "NULL":
                keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="редактировать 2-го \U0001F476", callback_data="edit_second_child")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="добавить 3-го \U0001F476  ️➡️", callback_data="add_three_child_button")
                keyboard_four_child.button(text="удалить 3-го \U0001F476", callback_data="delete_child_three")
                keyboard_four_child.button(text="добавить 4-го \U0001F476  ️➡️", callback_data="add_four_child_button")
                keyboard_four_child.adjust(2)

            else:
                keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
                keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
                keyboard_four_child.button(text="редактировать 2-го \U0001F476", callback_data="edit_second_child")
                keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
                keyboard_four_child.button(text="редактировать 3-го \U0001F476", callback_data="edit_three_child")
                keyboard_four_child.button(text="удалить 3-го \U0001F476", callback_data="delete_child_three")
                keyboard_four_child.button(text="добавить 4-го \U0001F476  ️➡️", callback_data="add_four_child_button")
                keyboard_four_child.adjust(2)

            await message.answer(text="<b>\U0001F476 Дети:</b>" + "\n" +
                                      f"     ♻️ Город: <b>{city}</b>" + "\n" +
                                      f"     ♻️ Адресс: <b>{home_address}</b>" + "\n" +
                                      f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                      f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                      f" 1️⃣  ♻️ ФИО: <b>{child_name}</b> <b>{child_female}</b> <b>{child_patronymic}</b>"
                                      + "\n" +
                                      f"     ♻️ Дата рождения: <b>{child_birth_date}</b>" + "\n" +
                                      f" 2️⃣  ♻️ ФИО: <b>{two_child_name}</b> <b>{two_child_female}</b> "
                                      f"<b>{two_child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{two_child_birth_date}</b>" + "\n" +
                                      f" 3️⃣  ♻️ ФИО: <b>{three_child_name}</b> <b>{three_child_female}</b> "
                                      f"<b>{three_child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{three_child_birth_date}</b>",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard_four_child.as_markup())
        if four_child_name is not None:
            keyboard_four_child.button(text="редактировать 1-го \U0001F476", callback_data="edit_child")
            keyboard_four_child.button(text="удалить 1-го \U0001F476", callback_data="delete_child_one")
            keyboard_four_child.button(text="редактировать 2-го \U0001F476", callback_data="edit_second_child")
            keyboard_four_child.button(text="удалить 2-го \U0001F476", callback_data="delete_child_two")
            keyboard_four_child.button(text="редактировать 3-го \U0001F476", callback_data="edit_three_child")
            keyboard_four_child.button(text="удалить 3-го \U0001F476", callback_data="delete_child_three")
            keyboard_four_child.button(text="редактировать 4-го \U0001F476", callback_data="edit_four_child")
            keyboard_four_child.button(text="удалить 4-го \U0001F476", callback_data="delete_child_four")
            keyboard_four_child.adjust(2)
            await message.answer(text="<b>\U0001F476 Дети:</b>" + "\n" +
                                      f"     ♻️ Город: <b>{city}</b>" + "\n" +
                                      f"     ♻️ Адресс: <b>{home_address}</b>" + "\n" +
                                      f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                      f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                      f" 1️⃣  ♻️ ФИО: <b>{child_name}</b> <b>{child_female}</b> <b>{child_patronymic}</b>"
                                      + "\n" +
                                      f"     ♻️ Дата рождения: <b>{child_birth_date}</b>" + "\n" +
                                      f" 2️⃣  ♻️ ФИО: <b>{two_child_name}</b> <b>{two_child_female}</b> "
                                      f"<b>{two_child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{two_child_birth_date}</b>" + "\n" +
                                      f" 3️⃣  ♻️ ФИО: <b>{three_child_name}</b> <b>{three_child_female}</b> "
                                      f"<b>{three_child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{three_child_birth_date}</b>" + "\n" +
                                      f" 4️⃣  ♻️ ФИО: <b>{four_child_name}</b> <b>{four_child_female}</b> "
                                      f"<b>{four_child_patronymic}</b>" + "\n" +
                                      f"     ♻️ Дата рождения: <b>{four_child_birth_date}</b>",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard_four_child.as_markup())

            # УСЛОВИЯ ПОСЛЕ УДАЛЕНИЯ РЕБЕНКА ИЗ БД, ВЫВОД В КОНСОЛЬ
    except TypeError:
        await message.answer(text="Ошибка регистрации! Пройдите регистрацию!",
                             reply_markup=reply_menu())
