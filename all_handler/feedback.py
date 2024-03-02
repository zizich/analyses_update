import asyncio
import os
import platform

import aiogram.exceptions
import sqlite3 as sq
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_base import archive_db, connect_archive

system_info = platform.system()

router = Router()


# ===============================================================================================================
#                                                  ПОМОЩЬ - ОБРАТНАЯ СВЯЗЬ
# ===============================================================================================================
@router.message(F.text.in_('\U0001F4D7 Обратная связь'))
async def process_feedback(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="КАК ЗАРЕГИСТРИРОВАТЬСЯ? \U000023E9", callback_data="how_to_register")
    keyboard.button(text="АНАЛИЗЫ, АКЦИИ \U000023E9", callback_data="how_to_selected_analyses")
    keyboard.button(text="РАБОТА С КОРЗИНОЙ \U000023E9", callback_data="how_to_shop")
    keyboard.button(text="ЗАЯВКИ, АРХИВ \U000023E9", callback_data="any_process")
    keyboard.button(text="НЕТУ РЕЗУЛЬТАТОВ \U000023E9", callback_data="not_result")
    keyboard.adjust(1)
    await message.answer(text="\U0001F4CD В этом разделе не оформляется заявка, не производится поиск анализов!"
                              "\n======================="
                              "\n\U0001F4CD Если, у Вас возникли вопросы и/или трудности по "
                              "оформлению/заполнению заявки, обращайтесь Администратору "
                              "чат-бота в личных сообщениях! https://t.me/zizicheg"
                              "\nлибо можете проконсультироваться по телефону: 33-04-00",
                         reply_markup=keyboard.as_markup())


# РАБОТА С КНОПКАМИ ПОМОЩИ
@router.callback_query(lambda c: c.data == "back_to_help")
async def process_back_to_help(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="КАК ЗАРЕГИСТРИРОВАТЬСЯ? \U000023E9", callback_data="how_to_register")
    keyboard.button(text="АНАЛИЗЫ, АКЦИИ \U000023E9", callback_data="how_to_selected_analyses")
    keyboard.button(text="РАБОТА С КОРЗИНОЙ \U000023E9", callback_data="how_to_shop")
    keyboard.button(text="ЗАЯВКИ, АРХИВ \U000023E9", callback_data="any_process")
    keyboard.button(text="НЕТУ РЕЗУЛЬТАТОВ \U000023E9", callback_data="not_result")
    keyboard.adjust(1)
    await call.message.edit_text(text="Если, у Вас возникли вопросы и/или трудности по "
                                      "оформлению/заполнению заявки, обращайтесь Администратору "
                                      "чат-бота в личных сообщениях! https://t.me/zizicheg"
                                      "\nлибо можете проконсультироваться по телефону: 33-04-00",
                                 reply_markup=keyboard.as_markup())


# РАБОТА С КНОПКОЙ - НЕТУ РЕЗУЛЬТАТА
@router.callback_query(lambda c: c.data == "not_result")
async def process_not_result(call: CallbackQuery):
    user_id = call.message.chat.id

    keyboard = InlineKeyboardBuilder()
    try:
        archive_db.execute(f"""SELECT * FROM user_{user_id}""")

        for i, (date, name, analysis, price, address, city, delivery, comm, confirm, id_midwifery) in (
                enumerate(archive_db.fetchall(), start=1)):
            keyboard.button(text=f"{date.split('>>')[0]}", callback_data=f"notResult_{date}")

        keyboard.button(text="назад \U000023EE", callback_data="back_to_help")
        keyboard.adjust(1)
        await call.message.edit_text(text="\U0000203C Если, в списке нету даты забора, то проверьте вкладку "
                                          "\U0001F4D1<b>Заявки</b> => выберите заявку => нажмите на кнопку "
                                          "<b>выполнено</b> и возвращайтесь сюда."
                                          "\n\U0000203C Выберите заявку и отправьте запрос Администратору с целью "
                                          "уточнения о готовности или отсутствии результата анализов!",
                                     reply_markup=keyboard.as_markup())
    except (sq.OperationalError, IndexError, TypeError, AttributeError):

        keyboard.button(text="назад \U000023EE", callback_data="back_to_help")
        keyboard.adjust(1)
        await call.message.edit_text(text="\U0000203C Если, в списке нету даты забора, то проверьте вкладку "
                                          "\U0001F4D1<b>Заявки</b> => выберите заявку => нажмите на кнопку "
                                          "<b>выполнено</b> и возвращайтесь сюда.",
                                     reply_markup=keyboard.as_markup())


# РАБОТА С КНОПКОЙ - НЕТУ РЕЗУЛЬТАТА
@router.callback_query(lambda c: c.data.startswith("notResult_"))
async def process_not_result_info(call: CallbackQuery):
    user_id = call.message.chat.id
    date = call.data.strip("notResult_")

    archive_db.execute(f"""SELECT * FROM user_{user_id}""")

    message_archive = ""
    for i, (date_arch, name, analysis, price, address, city, delivery, comm, confirm,
            id_midwifery) in (enumerate(archive_db.fetchall(), start=1)):
        if date == date_arch:
            if confirm != "результаты отправлены \U0000203C":
                confirm_text = "\U0000203C Нету результата \U0000203C"
            else:
                confirm_text = confirm
            message_archive = (f"\U0001F4C6Дата: {date_arch}:"
                               f"\n \U0000267BЛичные данные: {name}"
                               f"\n \U0000267BАнализы: \n{analysis}"
                               f"\n \U0000267BГород: {city}"
                               f"\n \U0000267BСтатус: {confirm_text}"
                               f"\n-------------------------------------")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="отправить запрос", callback_data=f"sendRequest_{date}>>{user_id}")
    keyboard.button(text="назад \U000023EE", callback_data="not_result")
    keyboard.adjust(1)

    await call.message.answer(text=message_archive, reply_markup=keyboard.as_markup())


# РАБОТА С КНОПКОЙ - ОТПРАВКА ЗАПРОСА ОБ ОТСУТСТВИИ РЕЗУЛЬТАТА
@router.callback_query(lambda c: c.data.startswith("sendRequest_"))
async def process_not_result_info(call: CallbackQuery):
    user_id = call.message.chat.id
    date = (call.data.strip("sendRequest_")).split(">>")[0]

    archive_db.execute(f"""UPDATE user_{user_id} SET confirm = ? WHERE id_date = ?""", ("нету результата", date))
    connect_archive.commit()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад \U000023EE", callback_data=f"notResult_{date}")
    keyboard.adjust(1)
    await call.message.answer(text="Запрос отправлен! Администратор ответит в течении дня!",
                              reply_markup=keyboard.as_markup())


# РАБОТА С КНОПКАМИ ПОМОЩИ
@router.callback_query(lambda c: c.data in ["how_to_register", "how_to_selected_analyses",
                                            "how_to_shop", "any_process"])
async def process_help_buttons(call: CallbackQuery):
    video_path = ""
    if system_info == "Windows":
        if call.data == "how_to_register":
            # Путь к вашему видео
            video_path = 'D:/Pro/Analyses/manual/Register/reg_1.mp4'
        elif call.data == "how_to_selected_analyses":
            video_path = 'D:/Pro/Analyses/manual/Register/reg_2.mp4'
        elif call.data == "how_to_selected_analyses":
            video_path = 'D:/Pro/Analyses/manual/Register/reg_3.mp4'
        elif call.data == "how_to_selected_analyses":
            video_path = 'D:/Pro/Analyses/manual/Register/reg_4.mp4'
    elif system_info == "Linux":
        if call.data == "how_to_register":
            # Путь к вашему видео
            video_path = '/root/Analyses/manual/Register/reg_1.mp4'
        elif call.data == "how_to_selected_analyses":
            video_path = '/root/Analyses/manual/Register/reg_2.mp4'
        elif call.data == "how_to_selected_analyses":
            video_path = '/root/Analyses/manual/Register/reg_3.mp4'
        elif call.data == "how_to_selected_analyses":
            video_path = '/root/Analyses/manual/Register/reg_4.mp4'

    # Проверяем существование видео-файла
    if not os.path.exists(video_path):
        await call.message.answer(text="Видео-инструкция на этапе разработки/оформления. "
                                       "Обратитесь к Администратору группы!")
        return

    # Отправляем видео пользователю с обратным отсчетом
    countdown_cycle = ["\U0001F4A8"]

    done = True
    while done:
        # Запускаем отправку видео в отдельной корутине
        asyncio.create_task(send_video_with_countdown(video_path))

        await call.message.edit_text(text=f"Загрузка видео-инструкции...\U0001F691{''.join(countdown_cycle)}")
        # Обратный отсчет
        for i in range(22):
            if i < 20:
                if 4 == len(countdown_cycle):
                    countdown_cycle = ["\U0001F4A8"]
                else:
                    countdown_cycle.append("\U0001F4A8")

                countdown_text = f"Загрузка видео-инструкции...\U0001F691{''.join(countdown_cycle)}"

                try:
                    await call.message.edit_text(text=countdown_text)
                except aiogram.exceptions.AiogramError:
                    pass
            else:
                done = False
                break
            await asyncio.sleep(1)

        if not done:
            break


def send_video_with_countdown(video_path):
    # Задержка перед отправкой видео
    try:
        with open(video_path, 'rb'):
            return send_video_with_countdown(video_path=video_path)
    except FileNotFoundError:
        return "Видео-инструкция на этапе разработки/оформления. Обратитесь к Администратору группы!"
