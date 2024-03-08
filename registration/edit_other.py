from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import cursor_db, conn, job_db
from keyboard import edit_people

router = Router(name=__name__)
user_id_num = 0
send_id = ""  # для получения id пользователя в БД


@router.callback_query(F.data.startswith("people_"))
async def process_edit_name_one(call: CallbackQuery, state: FSMContext):
    global user_id_num
    user_id_num = call.data.split("people_")[1]
    await state.set_state(States.waiting_for_add_fio_people_one)
    await call.message.edit_text(text='Введите ФИО: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ 1-ГО ЧЕЛОВЕКА========
@router.message(States.waiting_for_add_fio_people_one)
async def process_edit_name_one(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_fio_people_one=message.text)
    await state.set_state(States.waiting_for_add_birth_date_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n========================="
                              '\nВведите дату рождения (дд.мм.гггг): ')


@router.message(States.waiting_for_add_birth_date_people_one)
async def process_edit_female_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_birth_date_people_one=message.text)
    await state.set_state(States.waiting_for_add_phone_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n========================="
                              '\nВведите номер телефона (8911-222-33-44):')


# изменить отчество первого ребенка 1-ГО ЧЕЛОВЕКА
@router.message(States.waiting_for_add_phone_people_one)
async def process_edit_patronymic_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_phone_people_one=message.text)
    await state.set_state(States.waiting_for_add_email_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_edit_phone_people_one']}"
                              f"\n========================="
                              '\nВведите e-mail (эл.почта): ')


@router.message(States.waiting_for_add_email_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_email_people_one=message.text)
    await state.set_state(States.waiting_for_add_address_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_edit_phone_people_one']}"
                              f"\n\u267B\uFE0F Эл.почта: {data['waiting_for_edit_email_people_one']}"
                              f"\n========================="
                              '\nВведите адрес (без города):')


@router.message(States.waiting_for_add_address_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_address_people_one=message.text)

    keyboard = InlineKeyboardBuilder()

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"addCity_{city}")

    keyboard.adjust(1)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_edit_phone_people_one']}"
                              f"\n\u267B\uFE0F Эл.почта: {data['waiting_for_edit_email_people_one']}"
                              f"\n\u267B\uFE0F Адрес: {data['waiting_for_edit_address_people_one']}"
                              f"\n========================="
                              '\nВыберите город:',
                         reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith('addCity_'))
async def add_all_info(call: CallbackQuery, state: FSMContext):
    global user_id_num
    user_id = call.message.chat.id
    city = call.data.split("addCity_")[1]
    data = await state.get_data()

    # Распаковываем значения из словаря
    fio = data['waiting_for_add_fio_people_one']
    birth_date = data['waiting_for_edit_birth_date_people_one']
    phone = data['waiting_for_edit_phone_people_one']
    email = data['waiting_for_edit_email_people_one']
    address = data['waiting_for_edit_address_people_one']

    # Обновляем базу данных
    cursor_db.execute(
        f"""INSERT OR IGNORE INTO users_{user_id} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (f"{user_id_num}", fio, birth_date, phone, email, city, address, None, None))
    conn.commit()
    user_id_num = 0
    await state.clear()
    await call.message.answer(text=f"Данные успешно сохранены")
    # await call.message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
    #                                f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
    #                                f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_edit_phone_people_one']}"
    #                                f"\n\u267B\uFE0F Эл.почта: {data['waiting_for_edit_email_people_one']}"
    #                                f"\n\u267B\uFE0F Город: {city}"
    #                                f"\n\u267B\uFE0F Адрес: {data['waiting_for_edit_address_people_one']}")


# ================================ УДАЛИТЬ  ЧЕЛОВЕКА ========================================
@router.callback_query(F.data == "delPeople_")
async def process_delete_people_one(call: CallbackQuery):
    user_id = call.message.chat.id
    num = call.data.split("deletePeople_")[1]

    cursor_db.execute(f"""DELETE FROM users_{user_id} WHERE user_id = ? """, (f"{num}",))
    conn.commit()

    await call.message.edit_text(text="удален!")


# ================================ Редактировать  ЧЕЛОВЕКА ========================================
@router.callback_query(F.data == "editPeople_")
async def process_edit_people(call: CallbackQuery):
    user_id = call.data.split("editPeople_")[1]
    await call.message.edit_text(text="Для редакции выберите кнопку:", reply_markup=await edit_people(user_id))


@router.callback_query(F.data.startswith("peopleName_"))
async def process_edit_name_one(call: CallbackQuery, state: FSMContext):
    global send_id
    send_id = call.data.split("peopleName_")[1]
    await state.set_state(States.waiting_for_edit_fio_people_one)
    await call.message.edit_text(text='Введите ФИО: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ 1-ГО ЧЕЛОВЕКА========
@router.message(States.waiting_for_edit_fio_people_one)
async def process_edit_name_one(message: Message, state: FSMContext):
    global send_id
    user_id = message.chat.id
    id_user = send_id
    await state.update_data(waiting_for_edit_name_people_one=message.text)
    cursor_db.execute(f"""UPDATE users_{user_id} SET fio = ? WHERE user_id = ?""",
                      (message.text, id_user))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data=f"editPeople_{id_user}")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()
    send_id = ""


# изменить дату рождения первого ребенка ЧЕЛОВЕКА
@router.callback_query(F.data.startswith("peopleBirth_"))
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    global send_id
    send_id = call.data.split("peopleBirth_")[1]
    await state.set_state(States.waiting_for_edit_birth_date_people_one)
    await call.message.edit_text(text='Введите дату рождения: (дд.мм.гггг) ')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ ДАТУ РОЖДЕНИЯ 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_birth_date_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    global send_id
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_birth_date_people_one=message.text)
    cursor_db.execute(f"""UPDATE users_{user_id} SET birth_date = ? WHERE user_id = ?""",
                      (message.text, send_id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data=f"editPeople_{send_id}")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()
    send_id = ""


# изменить номер телефона 1-ГО ЧЕЛОВЕКА

@router.callback_query(F.data.startswith("peoplePhone_"))
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    global send_id
    send_id = call.data.split("peoplePhone_")[1]
    await state.set_state(States.waiting_for_edit_phone_date_people_one)
    await call.message.edit_text(text='Введите номер телефона:')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ НОМЕРА ТЕЛЕФОНА 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_phone_date_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    global send_id
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_phone_date_people_one=message.text)
    cursor_db.execute(f"""UPDATE users_{user_id} SET phone = ? WHERE user_id = ?""",
                      (message.text, send_id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data=f"editPeople_{send_id}")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()
    send_id = ""


# изменить номер e-mail ЧЕЛОВЕКА

@router.callback_query(F.data.startswith("peopleEmail_"))
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    global send_id
    send_id = call.data.split("peoplePhone_")[1]
    await state.set_state(States.waiting_for_edit_email_date_people_one)
    await call.message.edit_text(text='Введите email: (info@info.in)')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ e-mail 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_email_date_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_email_date_people_one=message.text)
    global send_id
    user_id = message.chat.id
    cursor_db.execute(f"""UPDATE users_{user_id} SET email = ? WHERE user_id = ?""",
                      (message.text, send_id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data=f"editPeople_{send_id}")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()
    send_id = ""


# изменить номер адрес 1-ГО ЧЕЛОВЕКА
@router.callback_query(F.data.startswith("cityPeople_"))
async def process_city_people_one(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    id_user = call.data.split("cityPeople_")[1]

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cPeople_{city}={id_user}")

    keyboard.adjust(1)
    await call.message.edit_text(text="\U0001F3D8 Выберите населенный пункт:",
                                 reply_markup=await keyboard.as_markup())


@router.callback_query(F.data.startswith("cPeople_"))
async def process_add_city_people_one(call: CallbackQuery):
    user_id = call.message.chat.id
    city = (call.data.split("cPeople_")[1]).split("=")[0]
    id_user = (call.data.split("cPeople_")[1]).split("=")[1]
    # #1 проверяем инициализирован ли город?

    cursor_db.execute(f"""UPDATE users_{user_id} SET city = ? WHERE user_id = ?""",
                      (call.message.text, id_user))
    conn.commit()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data=f"editPeople_{id_user}")

    await call.message.answer(text=f"Город: {city} успешно сохранен!", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith("peopleAdress_"))
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    global send_id
    send_id = call.data.split("peopleAdress_")[1]

    await state.set_state(States.waiting_for_edit_address_date_people_one)
    await call.message.edit_text(text='Введите адрес забора биоматериалов: ')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ АДРЕСА 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_address_date_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    global send_id
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_address_date_people_one=message.text)
    cursor_db.execute(f"""UPDATE users_{user_id} SET address = ? WHERE user_id = ?""",
                      (message.text, send_id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data=f"editPeople_{send_id}")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()
    send_id = ""
