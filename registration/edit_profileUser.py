from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import cursor_db, conn, basket_db, job_db, conn_basket
from keyboard import kb_edit_profile
from keyboard.replykeyboard import reply_menu

router = Router(name=__name__)


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ПРОФИЛЬ"=====================================
@router.callback_query(F.data == "edit_profile")
async def process_edit_profile(call: CallbackQuery):
    await call.message.answer(text="Редактировать данные: ", reply_markup=kb_edit_profile.kb_editProfile.as_markup())


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ИМЯ"=====================================
@router.callback_query(F.data == "edit_name_user")
async def process_edit_name_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_name_user)
    await call.message.answer(text='Введите имя:')


# ===============================ОБРАБОТКА КНОПКИ "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ==========================
@router.message(States.waiting_for_edit_name_user)
async def process_edit_name_user_back(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_name_user=message.text)
    cursor_db.execute("""UPDATE users SET name = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="Данные успешно сохранены!")


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ФАМИЛИЮ"=====================================
@router.callback_query(F.data == "edit_female_user")
async def process_edit_female_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_female_user)
    await call.message.answer(text='Введите фамилию:')


# ===============================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ==========================
@router.message(States.waiting_for_edit_female_user)
async def process_edit_female_user_back(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_female_user=message.text)
    cursor_db.execute("""UPDATE users SET female = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="Данные успешно сохранены!")


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ОТЧЕСТВО"=====================================
@router.callback_query(F.data == "edit_patronymic_user")
async def process_edit_patronymic_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_patronymic_user)
    await call.message.answer(text='Введите отчество:')


# ===============================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_patronymic_user)
async def process_edit_patronymic_user_back(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_patronymic_user=message.text)
    cursor_db.execute("""UPDATE users SET patronymic = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="Данные успешно сохранены!")


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ДАТУ РОЖДЕНИЯ"=====================================
@router.callback_query(F.data == "edit_birth_date_user")
async def process_edit_birth_date_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_birth_date_user)
    await call.message.answer(text='Введите дату рождения: (дд.мм.гггг.)')


# ===============================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ДАТЫ РОЖДЕНИЯ==========================
@router.message(States.waiting_for_edit_birth_date_user)
async def process_edit_birth_date_user_back(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_birth_date_user=message.text)
    cursor_db.execute("""UPDATE users SET birth_date = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="Данные успешно сохранены!")


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ НОМЕР ТЕЛЕФОНА"================================
@router.callback_query(F.data == "edit_phone_user")
async def process_edit_phone_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_phone_user)
    await call.message.answer(chat_id=call.message.chat.id,
                              text='Введите номер телефона в формате 8911-222-33-44')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ НОМЕРА ТЕЛЕФОНА==========================
@router.message(States.waiting_for_edit_phone_user)
async def process_edit_phone_user_back(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_phone_user=message.text)
    cursor_db.execute("""UPDATE users SET phone = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="Данные успешно сохранены!")


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ АДРЕСС ЭЛЕКТРОНОЙ ПОЧТЫ"=========================
@router.callback_query(F.data == "edit_email_user")
async def process_edit_email_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_email_user)
    await call.message.answer(text='Введите e-mail: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ЭЛЕКТРОННОЙ ПОЧТЫ========================
@router.message(States.waiting_for_edit_email_user)
async def process_edit_email_user_back(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_email_user=message.text)
    cursor_db.execute("""UPDATE users SET email = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="Данные успешно сохранены!")


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ГОРОД"=========================
@router.callback_query(F.data == "edit_city_user")
async def process_edit_city_user(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityEdit_{city}")

    keyboard.adjust(1)
    await call.message.answer(text="\U0001F3D8 Выберите город:", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith("cityEdit_"))
async def process_add_city(call: CallbackQuery):
    user_id = call.message.chat.id

    try:
        city_found = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""",
                                       (user_id,)).basket_db.fetchone()[0]

        basket_db.execute("""UPDATE users SET city = ? WHERE user_id = ?""", (None, user_id))
        conn_basket.commit()
        city_found.clear()
    except (TypeError, AttributeError):
        pass

    city = call.data.split("cityEdit_")[1]

    basket_db.execute("""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    conn_basket.commit()

    cursor_db.execute(f"""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    conn.commit()

    await call.message.answer(text=f"Город: {city} успешно сохранен!")


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ АДРЕСС ЗАБОРА КРОВИ"=========================
@router.callback_query(F.data == "edit_address_user")
async def process_edit_address_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_address_user)
    await call.message.answer(text='Введите адрес в формате: ул. Ленина д. 20 - 354')


# =================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ АДРЕСА ЗАБОРА КРОВИ========================
@router.message(States.waiting_for_edit_address_user)
async def process_edit_edit_address_user(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_address_user=message.text)
    cursor_db.execute("""UPDATE users SET address = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await state.clear()
    await message.answer(text="&#128657")
    await message.answer(text="Данные успешно сохранены!",
                         reply_markup=reply_menu())
