import sqlite3

from aiogram import Router
from aiogram.fsm.context import FSMContext

from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.fsm_engine import States

from data_base import database_db, connect_database
from keyboard.replykeyboard import reply_keyboard_menu

router = Router(name=__name__)


@router.message(CommandStart())
async def process_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        database_db.execute("SELECT fio, birth_date, phone, email, city, address"
                            f" FROM users WHERE user_id = ?", (user_id,))
        user = database_db.fetchall()
        for i, (fio, birth_date, phone, email, city, address) in enumerate(user, start=1):
            if city is None:
                keyboard = InlineKeyboardBuilder()
                keyboard.button(text="выберите город \U0001F3D8", callback_data="button_sub")
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n<b>==============================</b>"
                                          "\n\u203C \uFE0F<b>Выберите город. Нажмите на кнопку!:</b> ",
                                     reply_markup=keyboard.as_markup())
            elif fio is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_fio)
                await message.answer(text="\u203C\uFE0F<b>Введите ФИО:</b> ")
            elif birth_date is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_birth_day)
                await message.answer(text='Введите дату рождения - дд.мм.гггг: ')
            elif phone is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n    \u267B \uFE0FДата рождения: <b>{birth_date}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_phone)
                await message.answer(text='Введите номер телефона - 8911-222-33-44:')
            elif email is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n    \u267B \uFE0FДата рождения: <b>{birth_date}</b>"
                                          f"\n    \u267B \uFE0FНомер телефона: <b>{phone}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_email)
                await message.answer(text='Введите e-mail:')
            elif address is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n    \u267B \uFE0FДата рождения: <b>{birth_date}</b>"
                                          f"\n    \u267B \uFE0FНомер телефона: <b>{phone}</b>"
                                          f"\n    \u267B \uFE0FE-mail: <b>{email}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_address)
                await message.answer(text=f'Город: {city} \nВведите адрес в формате '
                                          f'(ул. Ленина, д.56-327)')
            else:
                await message.answer(text="\U0001F52C")
                await message.answer(text="\u267B \uFE0F Добро пожаловать!",
                                     reply_markup=reply_keyboard_menu)
    except (sqlite3.OperationalError, TypeError):
        # логика: в БД added_analysis.db будем создавать каждый раз таблицу индивидуальную для каждого пользователя
        # и будем добавлять туда выбранный анализ

        database_db.execute(f"""INSERT OR IGNORE INTO users (user_id) VALUES (?)""", (user_id,))
        connect_database.commit()

        # try:
        database_db.execute("SELECT fio, birth_date, phone, email, address, city"
                            f" FROM users WHERE user_id = ?", (user_id,))
        user = connect_database.fetchall()

        for i, (fio, birth_date, phone, email, address, city) in enumerate(user, start=1):
            if city is None:
                keyboard = InlineKeyboardBuilder()
                keyboard.button(text="выберите город \U0001F3D8", callback_data="button_sub")
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n<b>==============================</b>"
                                          "\n\u203C \uFE0F<b>Выберите город. Нажмите на кнопку!:</b> ",
                                     reply_markup=keyboard.as_markup())
            elif fio is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_fio)
                await message.answer(text="\u203C\uFE0F<b>Введите ФИО:</b> ")
            elif birth_date is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_birth_day)
                await message.answer(text='Введите дату рождения - дд.мм.гггг:')
            elif phone is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n    \u267B \uFE0FДата рождения: <b>{birth_date}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_phone)
                await message.answer(text='Введите номер телефона - 8911-222-33-44:')
            elif email is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n    \u267B \uFE0FДата рождения: <b>{birth_date}</b>"
                                          f"\n    \u267B \uFE0FНомер телефона: <b>{phone}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_email)
                await message.answer(text='Введите e-mail:')
            elif address is None:
                await message.answer(text="Для доступа к сервисам медицинских услуг, "
                                          "пожалуйста, пройдите регистрацию!"
                                          "\n\U0001F3E0<b>Профиль:</b>"
                                          f"\n    \u267B \uFE0FГород: <b>{city}</b>"
                                          f"\n    \u267B \uFE0FВаш id: <b>{user_id}</b>"
                                          f"\n    \u267B \uFE0FФИО: <b>{fio}</b>"
                                          f"\n    \u267B \uFE0FДата рождения: <b>{birth_date}</b>"
                                          f"\n    \u267B \uFE0FНомер телефона: <b>{phone}</b>"
                                          f"\n    \u267B \uFE0FE-mail: <b>{email}</b>"
                                          f"\n<b>==============================</b>")
                await state.set_state(States.waiting_for_address)
                await message.answer(text=f'Город: {city} \nВведите адрес в формате '
                                          f'(ул. Ленина, д.56-327)')

# @router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
# async def on_user_leave(event: ChatMemberUpdated):
#     await event.answer(text="Ждём Вас снова")
#
#
# @router.message(F.text == "Как дела?")
# async def process_help(message: Message):
#     await message.answer("Да, нормально! Сам как?")
#
#
# @router.message(F.photo)
# async def process_photo(message: Message):
#     await message.answer(f"Фото: {message.photo[-1].file_id}")
#
#
# @router.message(Command('get_photo'))
# async def process_get_photo(message: Message):
#     await message.answer_photo(
#         photo="https://cdn.pixabay.com/photo/2023/10/24/09/23/black-peppercorn-8337820_1280.jpg",
#         caption="Это логотип наш")
#
#
# # @router.message(Command('help'))
# # async def process_help(message: Message):
# #     await message.answer(f"Твой ID: {message.chat.id}"
# #                          f"\nИмя: {message.from_user.first_name}")
#
#
# @router.message(Command('help'))
# async def process_help(message: Message):
#     count = 10
#     text = "- " * count
#     message_id = await message.answer(text)
#     for i in range(count):
#         text = text.replace("-", "*", 1)
#         await message.bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=message_id.message_id)
#         await asyncio.sleep(1)
