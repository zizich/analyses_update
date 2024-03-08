from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import cursor_db, conn, job_db, basket_db, conn_basket
from keyboard import edit_people, choice_city

router = Router(name=__name__)
user_id_num = 0


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
    await state.set_state(States.waiting_for_edit_birth_date_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n========================="
                              '\nВведите дату рождения (дд.мм.гггг): ')


@router.message(States.waiting_for_edit_birth_date_people_one)
async def process_edit_female_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_birth_date_people_one=message.text)
    await state.set_state(States.waiting_for_edit_phone_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n========================="
                              '\nВведите номер телефона (8911-222-33-44):')


# изменить отчество первого ребенка 1-ГО ЧЕЛОВЕКА
@router.message(States.waiting_for_edit_phone_people_one)
async def process_edit_patronymic_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_phone_people_one=message.text)
    await state.set_state(States.waiting_for_edit_email_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_edit_phone_people_one']}"
                              f"\n========================="
                              '\nВведите e-mail (эл.почта): ')


@router.message(States.waiting_for_edit_email_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_email_people_one=message.text)
    await state.set_state(States.waiting_for_edit_address_people_one)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_add_fio_people_one']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_edit_birth_date_people_one']}"
                              f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_edit_phone_people_one']}"
                              f"\n\u267B\uFE0F Эл.почта: {data['waiting_for_edit_email_people_one']}"
                              f"\n========================="
                              '\nВведите адрес (без города):')


@router.message(States.waiting_for_edit_address_people_one)
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



