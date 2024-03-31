import os
import sqlite3 as sq
import aiogram
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_base import database_db, connect_database

router = Router(name=__name__)


# ===============================================================================================================
#                                                  АРХИВ СОДЕРЖАНИЕ
#                                                  ОБРАБОТКА КНОПОК
# ===============================================================================================================

@router.message(F.text.in_('\U0001F5C3 Архив заявок'))
async def process_go_to_the_archive(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="сформировать архив \U0001F5C2", callback_data="watch_archive")
    keyboard.button(text="очистить архив \U0001F9FD", callback_data="delete_archive")
    keyboard.adjust(1)

    await message.answer(text="\U0001F449 Выберите: ", reply_markup=keyboard.as_markup())


# обработка кнопки показать архив - watch_archive
@router.callback_query(F.data == "watch_archive")
async def process_watch_archive(call: CallbackQuery):
    user_id = call.message.chat.id

    try:
        # Извлечение данных из базы данных
        database_db.execute(f"""SELECT * FROM users_archive WHERE users_id = ?""", (user_id,))
        data = database_db.fetchall()

        msg_archive = []

        message_text = ""
        for i, (date, users_id, nurse_id, name, analysis, price, address, city, delivery, comment, confirm) in (
                enumerate(data, start=1)):
            database_db.execute("""SELECT * FROM nurse WHERE nurse_id = ?""", (nurse_id,))
            found_midwifery = database_db.fetchall()
            for y, (user, name_in, female, patronymic, phone, city_in_mid) in enumerate(found_midwifery, start=1):
                message_text = (f"\nМед.сестра: {name_in} {patronymic} "
                                f"\nТел.: {phone} ")
            message_archive = (f"{i}) Дата: {date}:\n* Личные данные: {name}"
                               f"\n* Анализы: \n{analysis}"
                               f"\n* Сумма: {price} р."
                               f"\nГород: {city}, {address}"
                               f"\nСпособ заявки: {delivery}"
                               f"\nКомментарии: {comment}"
                               f"\nСтатус: {confirm}"
                               f"\n-------------------------------------"
                               f"\n{message_text}"
                               "\n==============================================")
            msg_archive.append(message_archive)

        all_archive = "\n".join(msg_archive)

        # Создание .txt файла и запись данных
        txt_filename = 'Архив_заявок.txt'
        with open(txt_filename, 'w') as file:
            file.write(all_archive)

        # Отправка .txt файла пользователю
        with open(txt_filename, 'rb'):
            await call.message.answer_document(document=FSInputFile(os.path.abspath(txt_filename)),
                                               caption="Загружено")

        # Удаление временного .txt файла
        os.remove(txt_filename)
    except (sq.OperationalError, aiogram.exceptions.TelegramBadRequest):
        await call.message.answer(text="Архив пустой!")


# очистить весь архив
@router.callback_query(F.data == "delete_archive")
async def process_delete_archive(call: CallbackQuery):
    user_id = call.message.chat.id
    database_db.execute(f"""DELETE FROM users_archive WHERE users_id = ?""", (user_id,))
    connect_database.commit()

    await call.message.answer(text="Архив заявок полностью очищен! \U0001F5D1")
