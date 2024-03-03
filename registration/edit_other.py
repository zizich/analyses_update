from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import cursor_db, conn, job_db, basket_db, conn_basket
from keyboard import edit_people_one, choice_city

router = Router(name=__name__)


@router.callback_query(lambda c: c.data in ["edit_people_one", "add_people_one"])
async def process_edit_people_one(call: CallbackQuery):

    await call.message.edit_text(text="Редактировать/Добавить: ", reply_markup=await edit_people_one())


@router.callback_query(F.data == "people_name_one")
async def process_edit_name_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_name_people_one)
    await call.message.edit_text(text='Введите имя: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ 1-ГО ЧЕЛОВЕКА========
@router.message(States.waiting_for_edit_name_people_one)
async def process_edit_name_one(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_name_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_name_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# изменить фамилию первого ребенка 1-ГО ЧЕЛОВЕКА
@router.callback_query(F.data == "people_female_one")
async def process_edit_female_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_female_people_one)
    await call.message.edit_text(text='Введите фамилию: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ 1-ГО ЧЕЛОВЕКА==========
@router.message(States.waiting_for_edit_female_people_one)
async def process_edit_female_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_female_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_female_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# изменить отчество первого ребенка 1-ГО ЧЕЛОВЕКА
@router.callback_query(F.data == "people_patronymic_one")
async def process_edit_patronymic_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_patronymic_people_one)
    await call.message.edit_text(text='Введите отчество: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА 1-ГО ЧЕЛОВЕКА==========
@router.message(States.waiting_for_edit_patronymic_people_one)
async def process_edit_patronymic_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_patronymic_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_patronymic_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# изменить дату рождения первого ребенка 1-ГО ЧЕЛОВЕКА
@router.callback_query(F.data == "people_birth_day_one")
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_birth_date_people_one)
    await call.message.edit_text(text='Введите дату рождения: (дд.мм.гггг) ')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ ДАТУ РОЖДЕНИЯ 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_birth_date_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_birth_date_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_birth_date_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# изменить номер телефона 1-ГО ЧЕЛОВЕКА

@router.callback_query(F.data == "people_phone_one")
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_phone_people_one)
    await call.message.edit_text(text='Введите номер телефона:')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ НОМЕРА ТЕЛЕФОНА 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_phone_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_phone_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_phone_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# изменить номер e-mail 1-ГО ЧЕЛОВЕКА

@router.callback_query(F.data == "people_email_one")
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_email_people_one)
    await call.message.edit_text(text='Введите email: (info@info.in)')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ e-mail 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_email_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_email_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_email_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# изменить номер адрес 1-ГО ЧЕЛОВЕКА
@router.callback_query(F.data == "city_people_one")
async def process_city_people_one(call: CallbackQuery):
    await call.message.edit_text(text="\U0001F3D8 Выберите населенный пункт:",
                                 reply_markup=await choice_city())


@router.callback_query(F.data.startswith("cityOtherAdd_"))
async def process_add_city_people_one(call: CallbackQuery):
    user_id = call.message.chat.id

    # #1 проверяем инициализирован ли город?

    try:
        city_found = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""",
                                       (user_id,)).basket_db.fetchone()[0]

        basket_db.execute("""DELETE city FROM users WHERE user_id = ?""", (user_id,))
        conn_basket.commit()
        city_found.clear()
    except (TypeError, AttributeError):
        pass

    city = call.data.split("cityOtherAdd_")[1]

    basket_db.execute("""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    conn_basket.commit()

    cursor_db.execute(f"""UPDATE users SET others_city = ? WHERE user_id = ?""", (city, user_id))
    conn.commit()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")

    await call.message.answer(text=f"Город: {city} успешно сохранен!", reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "people_adress_one")
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_address_people_one)
    await call.message.edit_text(text='Введите адрес забора биоматериалов: ')


# ==========================ОБРАБОТКА КНОПКИ РЕДАКТИРОВАНИЯ АДРЕСА 1-ГО ЧЕЛОВЕКА=======
@router.message(States.waiting_for_edit_address_people_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_address_people_one=message.text)
    cursor_db.execute("""UPDATE users SET others_address_one = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад", callback_data="edit_people_one")
    await message.answer(text="Сохранено", reply_markup=keyboard.as_markup())
    await state.clear()


# ================================ УДАЛИТЬ 1-го ЧЕЛОВЕКА ========================================
@router.callback_query(F.data == "delete_people_one")
async def process_delete_people_one(call: CallbackQuery):
    user_id = call.message.chat.id
    tables = ["others_name_one", "others_female_one", "others_patronymic_one", "others_birth_date_one",
              "others_phone_one", "others_email_one", "others_address_one"]

    for table in tables:
        cursor_db.execute(f"""UPDATE users SET {table} = NULL WHERE user_id = ? """, (user_id,))
        conn.commit()

    await call.message.edit_text(text="удален!")
