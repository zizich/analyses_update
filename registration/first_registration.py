import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import database_db, connect_database
from keyboard.replykeyboard import reply_keyboard_menu

router = Router(name=__name__)


# ======================================================================================================
#                                   РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ
# ======================================================================================================
# обработка кнопки name и вернуться в список заполнения
@router.callback_query(F.data == "button_sub")
async def process_add_city(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    database_db.execute("""SELECT * FROM cities_payment""")
    for i, (city, *_) in enumerate(database_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityAdd_{city}")

    keyboard.adjust(1)
    await call.message.answer(text="\U0001F3D8 Выберите город:", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith('cityAdd_'))
async def process_add_n_sortym(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id

    city = call.data.split("cityAdd_")[1]

    database_db.execute("""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    connect_database.commit()

    await state.set_state(States.waiting_for_fio)
    await call.message.answer(text=f"Выбрали: \U0001F3E8{city}"
                                   '\nВведите ФИО:')


# получение имени, сохранение имени, запрос фамилии
@router.message(States.waiting_for_fio)
async def process_set_name(message: Message, state: FSMContext):
    await state.update_data(waiting_for_fio=message.text)
    await state.set_state(States.waiting_for_birth_day)
    data = (await state.get_data())['waiting_for_fio']
    await message.answer(text=f"\u267B\uFE0F ФИО: {data}"
                              f"\n========================="
                              '\nВведите дату рождения - ДД.ММ.ГГГГ:')


# получение даты рождения, сохранения даты рождения, запрос номер телефона
@router.message(States.waiting_for_birth_day)
async def process_birth_day(message: Message, state: FSMContext):
    await state.update_data(waiting_for_birth_day=message.text)
    await state.set_state(States.waiting_for_phone)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_fio']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_birth_day']}"
                              f"\n========================="
                              '\nВведите номер телефона - 8911-222-33-44:')


# получение номера телефона, сохранение номера, запрос email адреса
@router.message(States.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    if re.match(r'^(\+7|8)\d{3}-\d{3}-\d{2}-\d{2}$', phone):
        await state.update_data(waiting_for_phone=message.text)
        await state.set_state(States.waiting_for_email)
        data = await state.get_data()
        await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_fio']}"
                                  f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_birth_day']}"
                                  f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_phone']}"
                                  f"\n========================="
                                  '\nВведите e-mail:')
    else:
        await message.reply("Ошибка! Пожалуйста, введите номер корректно."
                            "\nВведите номер телефона в формате 8911-222-33-44:")


# получение e-mail, сохранение e-mail, запрос адреса домашнего
@router.message(States.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    user_id = message.chat.id

    city = database_db.execute(f"""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
    await state.update_data(waiting_for_email=message.text)
    await state.set_state(States.waiting_for_address)
    data = await state.get_data()
    await message.answer(text=f"\u267B\uFE0F ФИО: {data['waiting_for_fio']}"
                              f"\n\u267B\uFE0F Дата рождения: {data['waiting_for_birth_day']}"
                              f"\n\u267B\uFE0F Номер телефона: {data['waiting_for_phone']}"
                              f"\n\u267B\uFE0F Эл.почта: {data['waiting_for_email']}"
                              f"\n========================="
                              f'\nВы выбрали город: {city} \nТеперь введите адрес в формате - '
                              f'ул. Ленина, д.00-000')


# получение адреса, сохранение адреса
@router.message(States.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(waiting_for_address=message.text)
    data = await state.get_data()
    # Распаковываем значения из словаря
    fio = data['waiting_for_fio']
    birth_date = data['waiting_for_birth_day']
    phone = data['waiting_for_phone']
    email = data['waiting_for_email']
    address = data['waiting_for_address']

    # Обновляем базу данных
    database_db.execute(
        f"""UPDATE users SET fio = ?, birth_date = ?, phone = ?, email = ?, address = ? 
            WHERE user_id = ?""", (fio, birth_date, phone, email, address, user_id))
    connect_database.commit()

    await state.update_data(waiting_for_address=message.text)
    await message.answer(text="\U0001F52C")
    await message.answer(text="\U0001F4A2 Краткая инструкция:"
                              "\n=========================="
                              "\n'\U0001F3E0 Мой профиль - для просмотра личных данных"
                              "\n--------------------------"
                              "\n\U0001F465 Другие профили - список анкет других людей"
                              "\n--------------------------"
                              "\n\U0001F489 Анализы - для поиска анализа"
                              "\n--------------------------"
                              "\n\U0001F6D2 Корзина - для оформления заявки"
                              "\n--------------------------"
                              "\n\U0001F6CD Акции - информация об акция"
                              "\n--------------------------"
                              "\n\U0001F4D1 Заявки - для просмотра заявок"
                              "\n--------------------------"
                              "\n\U0001F468\U0000200D\U00002695\U0000FE0F Врачи - информация о врачах"
                              "\n--------------------------"
                              "\n\U0001F5C3 Архив заявок - для просмотра выполненных заявок"
                              "\n--------------------------"
                              "\n\U0001F4D7 Обратная связь - контакт с нами, инструкции"
                              "\n--------------------------",
                         reply_markup=reply_keyboard_menu)
    await state.clear()
