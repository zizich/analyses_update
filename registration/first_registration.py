import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import cursor_db, conn, basket_db, job_db, conn_basket
from keyboard.replykeyboard import reply_menu

router = Router(name=__name__)


# ======================================================================================================
#                                   РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ
# ======================================================================================================
# обработка кнопки name и вернуться в список заполнения
@router.callback_query(F.data == "button_sub")
async def process_add_city(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityAdd_{city}")

    keyboard.adjust(1)
    await call.message.answer(text="\U0001F3D8 Выберите город:", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith('cityAdd_'))
async def process_add_n_sortym(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id

    city = call.data.split("cityAdd_")[1]

    basket_db.execute("""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    conn_basket.commit()

    cursor_db.execute(f"""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    conn.commit()
    await state.set_state(States.waiting_for_name)
    await call.message.answer(text=f"Выбрали: \U0001F3E8{city}")
    await call.message.answer(text='Введите имя:')


# получение имени, сохранение имени, запрос фамилии
@router.message(States.waiting_for_name)
async def process_set_name(message: Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await state.set_state(States.waiting_for_female)
    await message.answer(text='Введите фамилию:')


# получение фамилии, сохранение фамилии, запрос отчество
@router.message(States.waiting_for_female)
async def process_female(message: Message, state: FSMContext):
    await state.update_data(waiting_for_female=message.text)
    await state.set_state(States.waiting_for_patronymic)
    await message.answer(text='Введите отчество:')


# получение отчество, сохранение отчество, запрос даты рождения
@router.message(States.waiting_for_patronymic)
async def process_patronymic(message: Message, state: FSMContext):
    await state.update_data(waiting_for_patronymic=message.text)
    await state.set_state(States.waiting_for_birth_day)
    await message.answer(text='Введите дату рождения: (ДД.ММ.ГГГГ)')


# получение даты рождения, сохранения даты рождения, запрос номер телефона
@router.message(States.waiting_for_birth_day)
async def process_birth_day(message: Message, state: FSMContext):
    await state.update_data(waiting_for_birth_day=message.text)
    await state.set_state(States.waiting_for_phone)
    await message.answer(text='Введите номер телефона: (8911-222-33-44)')


# получение номера телефона, сохранение номера, запрос email адреса
@router.message(States.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    if re.match(r'^(\+7|8)\d{3}-\d{3}-\d{2}-\d{2}$', phone):
        await state.update_data(waiting_for_phone=message.text)
        await state.set_state(States.waiting_for_email)
        await message.answer(text='Введите e-mail: (informatica@info.in)')
    else:
        await message.reply("Ошибка! Пожалуйста, введите номер корректно."
                            "\nВведите номер телефона в формате: (8911-222-33-44)")


# получение e-mail, сохранение e-mail, запрос адреса домашнего
@router.message(States.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    user_id = message.chat.id

    city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
    await state.update_data(waiting_for_email=message.text)
    await state.set_state(States.waiting_for_address)
    await message.answer(text=f'Город: {city} \nВведите адрес в формате '
                              f'(ул. Ленина, д.56-327)')


# получение адреса, сохранение адреса
@router.message(States.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(waiting_for_address=message.text)
    keyboard = reply_menu()
    await message.answer(text="\U0001F52C")
    await message.answer(text="\U0001F4A2 Краткая инструкция:"
                              "\n=========================="
                              "\n'\U0001F3E0 Профиль - для просмотра личных данных"
                              "\n--------------------------"
                              "\n\U0001F476 Дети - для заполнения/просмотра данных для детей"
                              "\n--------------------------"
                              "\n\U0001F465 Остальным - для заполнения/просмотра данных для других людей"
                              "\n--------------------------"
                              "\n\U0001F489 Анализы - для поиска анализа, добавление их в корзину."
                              "\n--------------------------"
                              "\n\U0001F6D2 Корзина - для оформления заявки"
                              "\n--------------------------"
                              "\n\U0001F6CD Акции - для просмотра/добавление акции"
                              "\n--------------------------"
                              "\n\U0001F4D1 Заявки - для просмотра готовых заявок"
                              "\n--------------------------"
                              "\n\U0001F468\U0000200D\U00002695\U0000FE0F Врачи - информация о врачах"
                              "\n--------------------------"
                              "\n\U0001F5C3 Архив заявок - для просмотра выполненных заявок"
                              "\n--------------------------"
                              "\n\U0001F4D7 Обратная связь - контакт с нами, инструкции"
                              "\n--------------------------",
                         reply_markup=keyboard)
    data = await state.get_data()
    await state.clear()

    # Распаковываем значения из словаря
    name = data['waiting_for_name']
    female = data['waiting_for_female']
    patronymic = data['waiting_for_patronymic']
    birth_date = data['waiting_for_birth_day']
    phone = data['waiting_for_phone']
    email = data['waiting_for_email']
    address = data['waiting_for_address']

    # Обновляем базу данных
    cursor_db.execute(
        """UPDATE users SET name = ?, female = ?, patronymic = ?, birth_date = ?, phone = ?, email = ?, address = ? 
        WHERE user_id = ?""", (name, female, patronymic, birth_date, phone, email, address, user_id))
    conn.commit()



