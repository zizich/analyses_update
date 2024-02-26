from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import cursor_db, conn, basket_db, job_db, conn_basket
from keyboard import kb_edit_profile, buttons_edit_childs_one, buttons_edit_childs_two, buttons_edit_childs_three, \
    buttons_edit_childs_four
from keyboard.replykeyboard import reply_menu

router = Router(name=__name__)


# ================================ДОБАВЛЕНИЕ 1-го РЕБНКА ============================================
@router.callback_query(lambda c: c.data == "add_child_button")
async def process_add_child(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_add_child_button)
    await call.message.answer(text="Введите имя:")


# =====получаем имя, сохраняем и запрашиваем фамилию
@router.message(States.waiting_for_add_child_button)
async def process_add_name_child_button(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_child_button=message.text)
    await state.set_state(States.waiting_for_add_child_female_button)
    await message.answer(text="Введите фамилию: ")


# =====получаем ФАМИЛИЮ, сохраняем и запрашиваем ОТЧЕСТВО===============
@router.message(States.waiting_for_add_child_female_button)
async def process_add_female_child_button(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_child_female_button=message.text)
    await state.set_state(States.waiting_for_add_child_patronymic_button)
    await message.answer(text="Введите отчество: ")


# =====получаем ОТЧЕСТВО, сохраняем и запрашиваем ДАТУ РОЖДЕНИЯ===============
@router.message(States.waiting_for_add_child_patronymic_button)
async def process_add_patronymic_child_button(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_child_patronymic_button=message.text)
    await state.set_state(States.waiting_for_add_child_birth_date)
    await message.answer(text="Введите дату рождения: (дд.мм.гггг)")


# =====получаем ДАТУ РОЖДЕНИЯ, сохраняем  ===============
@router.message(States.waiting_for_add_child_birth_date)
async def process_add_child_birth_date_button(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(waiting_for_add_child_birth_date=message.text)
    await state.set_state(States.waiting_for_add_child_birth_date)
    await message.answer(text="Данные успешно сохранены!")

    data = await state.get_data()
    await state.clear()

    # Распаковываем значения из словаря
    name = data['waiting_for_add_child_button']
    female = data['waiting_for_add_child_female_button']
    patronymic = data['waiting_for_add_child_patronymic_button']
    birth_date = data['waiting_for_add_child_birth_date']

    # Обновляем базу данных
    cursor_db.execute("""UPDATE users SET child_name = ?, child_female = ?, child_patronymic = ?, child_birth_date = ? 
    WHERE user_id = ?""", (name, female, patronymic, birth_date, user_id))
    conn.commit()


# ======================================================================================================
#                                           Редактировать 1-го ребенка
# ======================================================================================================
@router.callback_query(lambda c: c.data == "edit_child")
async def process_edit_child(call: CallbackQuery, state: FSMContext):
    keyboard = buttons_edit_childs_one()
    await call.message.answer(text="Изменить 1-го ребенка: ", reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data == "name_one")
async def process_edit_name_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_child_name_one)
    await call.message.answer(text='Введите имя: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ==========================
@router.message(States.waiting_for_edit_child_name_one)
async def process_edit_name_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_child_name_one=message.text)
    cursor_db.execute("""UPDATE users SET child_name = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить фамилию первого ребенка
@router.callback_query(lambda c: c.data == "female_one")
async def process_edit_female_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_child_female_one)
    await call.message.answer(text='Введите фамилию: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ==========================
@router.message(States.waiting_for_edit_child_female_one)
async def process_edit_female_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_child_female_one=message.text)
    cursor_db.execute("""UPDATE users SET child_female = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    await message.answer(text="Сохранено")
    await state.clear()


# изменить отчество первого ребенка
@router.callback_query(lambda c: c.data == "patronymic_one")
async def process_edit_patronymic_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_child_patronymic_one)
    await call.message.answer(text='Введите отчество: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_child_patronymic_one)
async def process_edit_patronymic_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_child_patronymic_one=message.text)
    cursor_db.execute("""UPDATE users SET child_patronymic = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить дату рождения первого ребенка
@router.callback_query(lambda c: c.data == "birth_day_one")
async def process_edit_birth_day_one(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_child_birth_day_one)
    await call.message.answer(text='Введите дату рождения: (дд.мм.гггг) ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_child_birth_day_one)
async def process_edit_birth_day_one_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_child_birth_day_one=message.text)
    cursor_db.execute("""UPDATE users SET child_birth_date = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# ================================================================================================================
#                                                ДОБАВЛЕНИЕ 2-ГО РЕБЕНКА
# ================================================================================================================
@router.callback_query(lambda c: c.data == "add_two_child_button")
async def process_add_child_two(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_add_two_child_name)
    await call.message.answer(text="Введите имя:")


# =====получаем имя, сохраняем и запрашиваем фамилию 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_two_child_name)
async def process_add_name_child_button_two(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_two_child_name=message.text)
    await state.set_state(States.waiting_for_add_two_child_female)
    await message.answer(text="Введите фамилию: ")


# =====получаем ФАМИЛИЮ, сохраняем и запрашиваем ОТЧЕСТВО 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_two_child_female)
async def process_add_female_child_button_two(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_two_child_female=message.text)
    await state.set_state(States.waiting_for_add_two_child_patronymic)
    await message.answer(text="Введите отчество: ")


# =====получаем ОТЧЕСТВО, сохраняем и запрашиваем ДАТУ РОЖДЕНИЯ 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_two_child_patronymic)
async def process_add_patronymic_child_button_two(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_two_child_patronymic=message.text)
    await state.set_state(States.waiting_for_add_two_child_birth_date)
    await message.answer(text="Введите дату рождения: (дд.мм.гггг)")


# =====получаем ДАТУ РОЖДЕНИЯ, сохраняем 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_two_child_birth_date)
async def process_add_child_birth_date_button_two(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(waiting_for_add_two_child_birth_date=message.text)
    await message.answer(text="Данные успешно сохранены!")
    data = await state.get_data()
    await state.clear()

    name = data['waiting_for_add_two_child_name']
    female = data['waiting_for_add_two_child_female']
    patronymic = data['waiting_for_add_two_child_patronymic']
    birth_date = data['waiting_for_add_two_child_birth_date']

    cursor_db.execute("""UPDATE users SET two_child_name = ?, two_child_female = ?, two_child_patronymic = ?, 
    two_child_birth_date = ? WHERE user_id = ?""", (name, female, patronymic, birth_date, user_id))
    conn.commit()


# ======================================================================================================
#                                           Редактировать 2-го ребенка
# ======================================================================================================
@router.callback_query(lambda c: c.data == "edit_second_child")
async def process_edit_child_two(call: CallbackQuery):
    keyboard = buttons_edit_childs_two()
    await call.message.answer(text="Изменить 1-го ребенка: ", reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data == "name_two")
async def process_edit_name_two(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_two_child_name)
    await call.message.answer(text='Введите имя: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ==========================
@router.message(States.waiting_for_edit_two_child_name)
async def process_edit_name_two_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_two_child_name=message.text)
    cursor_db.execute("""UPDATE users SET two_child_name = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить фамилию первого ребенка
@router.callback_query(lambda c: c.data == "female_two")
async def process_edit_female_two(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_two_child_female)
    await call.message.answer(text='Введите фамилию: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ==========================
@router.message(States.waiting_for_edit_two_child_female)
async def process_edit_female_two_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_two_child_female=message.text)
    cursor_db.execute("""UPDATE users SET two_child_female = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    await message.answer(text="Сохранено")
    await state.clear()


# изменить отчество первого ребенка
@router.callback_query(lambda c: c.data == "patronymic_two")
async def process_edit_patronymic_two(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_two_child_patronymic)
    await call.message.answer(text='Введите отчество: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_two_child_patronymic)
async def process_edit_patronymic_two_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_two_child_patronymic=message.text)
    cursor_db.execute("""UPDATE users SET two_child_patronymic = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить дату рождения первого ребенка
@router.callback_query(lambda c: c.data == "birth_day_two")
async def process_edit_birth_day_two(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_two_child_birth_date)
    await call.message.answer(text='Введите дату рождения: (дд.мм.гггг) ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_two_child_birth_date)
async def process_edit_birth_day_two_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_two_child_birth_date=message.text)
    cursor_db.execute("""UPDATE users SET two_child_birth_date = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# ================================================================================================================
#                                                ДОБАВЛЕНИЕ 3-ГО РЕБЕНКА
# ================================================================================================================
@router.callback_query(lambda c: c.data == "add_three_child_button")
async def process_add_child_three(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_add_three_child_name)
    await call.message.answer(text="Введите имя:")


# =====получаем имя, сохраняем и запрашиваем фамилию 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_three_child_name)
async def process_add_name_child_button_three(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_three_child_name=message.text)
    await state.set_state(States.waiting_for_add_three_child_female)
    await message.answer(text="Введите фамилию: ")


# =====получаем ФАМИЛИЮ, сохраняем и запрашиваем ОТЧЕСТВО 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_three_child_female)
async def process_add_female_child_button_three(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_three_child_female=message.text)
    await state.set_state(States.waiting_for_add_three_child_patronymic)
    await message.answer(text="Введите отчество: ")


# =====получаем ОТЧЕСТВО, сохраняем и запрашиваем ДАТУ РОЖДЕНИЯ 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_three_child_patronymic)
async def process_add_patronymic_child_button_three(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_three_child_patronymic=message.text)
    await state.set_state(States.waiting_for_add_three_child_birth_date)
    await message.answer(text="Введите дату рождения: (дд.мм.гггг)")


# =====получаем ДАТУ РОЖДЕНИЯ, сохраняем 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_three_child_birth_date)
async def process_add_child_birth_date_button_three(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(waiting_for_add_three_child_birth_date=message.text)
    await message.answer(text="Данные успешно сохранены!")
    data = await state.get_data()
    await state.clear()

    name = data['waiting_for_add_three_child_name']
    female = data['waiting_for_add_three_child_female']
    patronymic = data['waiting_for_add_three_child_patronymic']
    birth_date = data['waiting_for_add_three_child_birth_date']

    cursor_db.execute("""UPDATE users SET three_child_name = ?, three_child_female = ?, three_child_patronymic = ?, 
    three_child_birth_date = ? WHERE user_id = ?""", (name, female, patronymic, birth_date, user_id))
    conn.commit()


# ======================================================================================================
#                                           Редактировать 3-ГО РЕБЕНКА
# ======================================================================================================
@router.callback_query(lambda c: c.data == "edit_three_child")
async def process_edit_child_three(call: CallbackQuery):
    keyboard = buttons_edit_childs_three()
    await call.message.answer(text="Изменить 3-го ребенка: ", reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data == "name_three")
async def process_edit_name_three(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_three_child_name)
    await call.message.answer(text='Введите имя: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ==========================
@router.message(States.waiting_for_edit_three_child_name)
async def process_edit_name_three_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_three_child_name=message.text)
    cursor_db.execute("""UPDATE users SET three_child_name = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить фамилию первого ребенка
@router.callback_query(lambda c: c.data == "female_three")
async def process_edit_female_three(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_three_child_female)
    await call.message.answer(text='Введите фамилию: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ==========================
@router.message(States.waiting_for_edit_three_child_female)
async def process_edit_female_one_three(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_three_child_female=message.text)
    cursor_db.execute("""UPDATE users SET three_child_female = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    await message.answer(text="Сохранено")
    await state.clear()


# изменить отчество первого ребенка
@router.callback_query(lambda c: c.data == "patronymic_three")
async def process_edit_patronymic_three(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_three_child_patronymic)
    await call.message.answer(text='Введите отчество: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_three_child_patronymic)
async def process_edit_patronymic_three_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_three_child_patronymic=message.text)
    cursor_db.execute("""UPDATE users SET three_child_patronymic = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить дату рождения первого ребенка
@router.callback_query(lambda c: c.data == "birth_day_three")
async def process_edit_birth_day_three(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_three_child_birth_date)
    await call.message.answer(text='Введите дату рождения: (дд.мм.гггг) ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_three_child_birth_date)
async def process_edit_birth_day_three_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_three_child_birth_date=message.text)
    cursor_db.execute("""UPDATE users SET three_child_birth_date = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# ================================================================================================================
#                                                ДОБАВЛЕНИЕ 4-ГО РЕБЕНКА
# ================================================================================================================
@router.callback_query(lambda c: c.data == "add_four_child_button")
async def process_add_child_four(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_add_four_child_name)
    await call.message.answer(text="Введите имя:")


# =====получаем имя, сохраняем и запрашиваем фамилию 4-ГО РЕБЕНКА
@router.message(States.waiting_for_add_four_child_name)
async def process_add_name_child_button_four(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_four_child_name=message.text)
    await state.set_state(States.waiting_for_add_four_child_female)
    await message.answer(text="Введите фамилию: ")


# =====получаем ФАМИЛИЮ, сохраняем и запрашиваем ОТЧЕСТВО 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_four_child_female)
async def process_add_female_child_button_four(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_four_child_female=message.text)
    await state.set_state(States.waiting_for_add_four_child_patronymic)
    await message.answer(text="Введите отчество: ")


# =====получаем ОТЧЕСТВО, сохраняем и запрашиваем ДАТУ РОЖДЕНИЯ 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_four_child_patronymic)
async def process_add_patronymic_child_button_four(message: Message, state: FSMContext):
    await state.update_data(waiting_for_add_four_child_patronymic=message.text)
    await state.set_state(States.waiting_for_add_four_child_birth_date)
    await message.answer(text="Введите дату рождения: (дд.мм.гггг)")


# =====получаем ДАТУ РОЖДЕНИЯ, сохраняем 2-ГО РЕБЕНКА
@router.message(States.waiting_for_add_four_child_birth_date)
async def process_add_child_birth_date_button_four(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(waiting_for_add_four_child_birth_date=message.text)
    await message.answer(text="Данные успешно сохранены!")
    data = await state.get_data()
    await state.clear()

    name = data['waiting_for_add_four_child_name']
    female = data['waiting_for_add_four_child_female']
    patronymic = data['waiting_for_add_four_child_patronymic']
    birth_date = data['waiting_for_add_four_child_birth_date']

    cursor_db.execute("""UPDATE users SET four_child_name = ?, four_child_female = ?, four_child_patronymic = ?, 
    four_child_birth_date = ? WHERE user_id = ?""", (name, female, patronymic, birth_date, user_id))
    conn.commit()


# ======================================================================================================
#                                           Редактировать 4-ГО РЕБЕНКА
# ======================================================================================================
@router.callback_query(lambda c: c.data == "edit_four_child")
async def process_edit_child_four(call: CallbackQuery):
    keyboard = buttons_edit_childs_four()
    await call.message.answer(text="Изменить 4-го ребенка: ", reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data == "name_four")
async def process_edit_name_four(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_four_child_name)
    await call.message.answer(text='Введите имя: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ==========================
@router.message(States.waiting_for_edit_four_child_name)
async def process_edit_name_four_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_four_child_name=message.text)
    cursor_db.execute("""UPDATE users SET four_child_name = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить фамилию первого ребенка
@router.callback_query(lambda c: c.data == "female_four")
async def process_edit_female_four(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_four_child_female)
    await call.message.answer(text='Введите фамилию: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ==========================
@router.message(States.waiting_for_edit_four_child_female)
async def process_edit_female_one_four(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_four_child_female=message.text)
    cursor_db.execute("""UPDATE users SET four_child_female = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    await message.answer(text="Сохранено")
    await state.clear()


# изменить отчество первого ребенка
@router.callback_query(lambda c: c.data == "patronymic_four")
async def process_edit_patronymic_four(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_four_child_patronymic)
    await call.message.answer(text='Введите отчество: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_four_child_patronymic)
async def process_edit_patronymic_four_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_four_child_patronymic=message.text)
    cursor_db.execute("""UPDATE users SET four_child_patronymic = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# изменить дату рождения первого ребенка
@router.callback_query(lambda c: c.data == "birth_day_four")
async def process_edit_birth_day_four(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_four_child_birth_date)
    await call.message.answer(text='Введите дату рождения: (дд.мм.гггг) ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ОТЧЕСТВА==========================
@router.message(States.waiting_for_edit_four_child_birth_date)
async def process_edit_birth_day_four_done(message: Message, state: FSMContext):
    await state.update_data(waiting_for_edit_four_child_birth_date=message.text)
    cursor_db.execute("""UPDATE users SET four_child_birth_date = ? WHERE user_id = ?""",
                      (message.text, message.from_user.id))
    conn.commit()
    await message.answer(text="Сохранено")
    await state.clear()


# ========================================================================================
#                                      УДАЛЕНИЕ 1-го ребенка
# ========================================================================================
@router.callback_query(lambda c: c.data == "delete_child_one")
async def process_delete_child_one(call: CallbackQuery):
    user_id = call.message.chat.id
    tables = ["child_name", "child_female", "child_patronymic", "child_birth_date",
              "child_subscribe_date_analysis", "child_subscribe_date_doctor", "child_photo_analysis"]

    for table in tables:
        cursor_db.execute(f"""UPDATE users SET {table} = NULL WHERE user_id = ? """, (user_id,))
    conn.commit()

    await call.message.answer(text="удален 1-й ребенок!")


# ========================================================================================
#                                      УДАЛЕНИЕ 2-го ребенка
# ========================================================================================
@router.callback_query(lambda c: c.data == "delete_child_two")
async def process_delete_child_one(call: CallbackQuery):
    user_id = call.message.from_user.id
    tables = ["two_child_name", "two_child_female", "two_child_patronymic", "two_child_birth_date",
              "two_child_subscribe_date_analysis", "two_child_subscribe_date_doctor", "two_child_photo_analysis"]

    for table in tables:
        cursor_db.execute(f"""UPDATE users SET {table} = NULL WHERE user_id = ? """, (user_id,))
    conn.commit()

    await call.message.answer(text="удален 2-й ребенок!")


# ========================================================================================
#                                      УДАЛЕНИЕ 3-го ребенка
# ========================================================================================
@router.callback_query(lambda c: c.data == "delete_child_three")
async def process_delete_child_one(call: CallbackQuery):
    user_id = call.message.from_user.id
    tables = ["three_child_name", "three_child_female", "three_child_patronymic", "three_child_birth_date",
              "three_child_subscribe_date_analysis", "three_child_subscribe_date_doctor", "three_child_photo_analysis"]

    for table in tables:
        cursor_db.execute(f"""UPDATE users SET {table} = NULL WHERE user_id = ? """, (user_id,))
    conn.commit()

    await call.message.answer(text="удален 3-й ребенок!")


# ========================================================================================
#                                      УДАЛЕНИЕ 4-го ребенка
# ========================================================================================
@router.callback_query(F.data.startswish("delete_child_four"))
async def process_delete_child_one(call: CallbackQuery):
    user_id = call.message.from_user.id
    tables = ["four_child_name", "four_child_female", "four_child_patronymic", "four_child_birth_date",
              "four_child_subscribe_date_analysis", "four_child_subscribe_date_doctor", "four_child_photo_analysis"]

    for table in tables:
        cursor_db.execute(f"""UPDATE users SET {table} = NULL WHERE user_id = ? """, (user_id,))
    conn.commit()

    await call.message.answer(text="удален 4-й ребенок!")
