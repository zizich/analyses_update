import queries.user as query

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.fsm_engine import States
from keyboard import edit_user
from keyboard.replykeyboard import reply_keyboard_menu


router = Router(name=__name__)


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ПРОФИЛЬ"=====================================
@router.callback_query(F.data == "edit_profile")
async def process_edit_profile(call: CallbackQuery):
    await call.message.edit_text(text="Редактировать данные: ", reply_markup=await edit_user())


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ИМЯ"=====================================
@router.callback_query(F.data == "edit_fio_user")
async def process_edit_name_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_fio_user)
    await call.message.edit_text(text='Редактирование основного профиля:'
                                      '\nВведите ФИО:')


# ===============================ОБРАБОТКА КНОПКИ "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ИМЕНИ==========================
@router.message(States.waiting_for_edit_fio_user)
async def process_edit_name_user_back(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_fio_user=message.text)

    query.edit_fio_users(user_id, message.text)

    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text="назад", callback_data="edit_profile")
    await message.answer(text="Данные успешно сохранены!", reply_markup=kb.adjust(1).as_markup())


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ДАТУ РОЖДЕНИЯ"=====================================
@router.callback_query(F.data == "edit_birth_date_user")
async def process_edit_birth_date_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_birth_date_user)
    await call.message.edit_text(text='Редактирование основного профиля:'
                                      '\nВведите дату рождения: (дд.мм.гггг.)')


# ===============================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ДАТЫ РОЖДЕНИЯ==========================
@router.message(States.waiting_for_edit_birth_date_user)
async def process_edit_birth_date_user_back(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_birth_date_user=message.text)

    query.edit_birth_date_users(user_id, message.text)

    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text="назад", callback_data="edit_profile")
    await message.answer(text="Данные успешно сохранены!", reply_markup=kb.adjust(1).as_markup())


# ==================================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ НОМЕР ТЕЛЕФОНА"================================
@router.callback_query(F.data == "edit_phone_user")
async def process_edit_phone_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_phone_user)
    await call.message.edit_text(text='Редактирование основного профиля:'
                                      '\nВведите номер телефона в формате 8911-222-33-44')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ НОМЕРА ТЕЛЕФОНА==========================
@router.message(States.waiting_for_edit_phone_user)
async def process_edit_phone_user_back(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_phone_user=message.text)

    query.edit_phone_users(user_id, message.text)

    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text="назад", callback_data="edit_profile")
    await message.answer(text="Данные успешно сохранены!", reply_markup=kb.adjust(1).as_markup())


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ АДРЕСС ЭЛЕКТРОНОЙ ПОЧТЫ"=========================
@router.callback_query(F.data == "edit_email_user")
async def process_edit_email_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_email_user)
    await call.message.edit_text(text='Редактирование основного профиля:'
                                      '\nВведите e-mail: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ЭЛЕКТРОННОЙ ПОЧТЫ========================
@router.message(States.waiting_for_edit_email_user)
async def process_edit_email_user_back(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_email_user=message.text)

    query.edit_email_users(user_id, message.text)

    await state.clear()
    kb = InlineKeyboardBuilder()
    kb.button(text="назад", callback_data="edit_profile")
    await message.answer(text="Данные успешно сохранены!", reply_markup=kb.adjust(1).as_markup())


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ ГОРОД"=========================
@router.callback_query(F.data == "edit_city_user")
async def process_edit_city_user(call: CallbackQuery):
    await call.message.edit_text(text="\U0001F3D8 Выберите город:", reply_markup=await query.edit_city_users())


@router.callback_query(F.data.startswith("cityEdit_"))
async def process_add_city(call: CallbackQuery):
    user_id = call.message.chat.id

    city = call.data.split("cityEdit_")[1]

    query.set_city_basket(city, user_id)
    query.set_city_users(city, user_id)

    kb = InlineKeyboardBuilder()
    kb.button(text="назад", callback_data="edit_profile")
    await call.message.answer(text=f"Город: {city} успешно сохранен!", reply_markup=kb.adjust(1).as_markup())


# =============================ОБРАБОТКА КНОПКИ "РЕДАКТИРОВАТЬ АДРЕСС ЗАБОРА КРОВИ"=========================
@router.callback_query(F.data == "edit_address_user")
async def process_edit_address_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_edit_address_user)
    await call.message.edit_text(text='Редактирование основного профиля:'
                                      '\nВведите адрес в формате: ул. Ленина д. 20 - 354')


# =================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ АДРЕСА ЗАБОРА КРОВИ========================
@router.message(States.waiting_for_edit_address_user)
async def process_edit_edit_address_user(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.update_data(waiting_for_edit_address_user=message.text)

    query.edit_address_users(user_id, message.text)

    await state.clear()
    await message.answer(text="&#128657")
    await message.answer(text="Данные успешно сохранены!",
                         reply_markup=reply_keyboard_menu)
