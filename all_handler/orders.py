from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States
from data_base import (basket_db, conn_basket, job_db, date_add_db, midwifery_conn, pattern_db, all_analysis_db,
                       connect_pattern, profit_income_db, connect_profit_income, order_done_db, connect_order_done)

router = Router(name=__name__)

button_not_duplicate = []
transfer_date_delivery = ""


@router.message(F.text.in_('\U0001F4D1 Заявки'))
@router.callback_query(lambda c: c.data == "back_to_orders")
async def process_back_to_confirm_orders(call: CallbackQuery):
    user_id = call.message.chat.id

    global button_not_duplicate, transfer_date_delivery

    # TODO выводим все данные с БД basket пользователя на консоль
    basket_db.execute(f"SELECT * FROM user_{user_id}")
    result_the_end = basket_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (id_date, name, analysis, price, address, city, delivery, comm, id_mid, confirm) in enumerate(result_the_end,
                                                                                                         start=1):

        if confirm == "не подтверждена":
            emoji_str = "\U0000274C"
        else:
            emoji_str = "\u2705"
        keyboard.button(text=f"{id_date.split('>>')[0]}   {emoji_str}", callback_data=f"ordersShow_{id_date}")

   keyboard.adjust(1)

    if len(result_the_end) != 0 and result_the_end[0][0] is not None:
        await call.message.chat(text="\U0001F449 Выберите заявку: ", reply_markup=keyboard)
    else:
        await bot.edit_message_text(text="Заявок нет!")


# ==========================================================================================================
# ОБРАБОТКА ВЫБРАННОЙ и ПОДТВЕРЖДЕННОЙ ЗАЯВКИ (ОПЛАТА, УДАЛИТЬ, НАЗАД В КОРЗИНУ)
@router.callback_query_handler(lambda c: c.data.startswith("ordersShow_"))
async def processing_in_confirm_date(call: types.CallbackQuery):
    global transfer_date, back_to_setting_analyses, message_text_setting_orders
    user_id = call.message.chat.id
    back_to_setting_analyses = call.data.split("ordersShow_")[1]

    # выводим данные из стоимости услуг компании

    cash_phone_bank = ""
    confirm_order = ""
    date = ""

    # выводим все данные с БД basket пользователя на консоль
    basket_db.execute(f"SELECT * FROM user_{user_id}")
    result_the_end = basket_db.fetchall()
    for i, (id_date, name, analysis, price, address, city, delivery, comm, id_num, confirm) in enumerate(result_the_end,
                                                                                                         start=1):

        phone = job_db.execute("""SELECT phone FROM services WHERE city = ?""", (city,)).fetchone()[0]
        bank = job_db.execute("""SELECT bank FROM services WHERE city = ?""", (city,)).fetchone()[0]

        cash_phone_bank = ("\n==========================="
                           "\n<b>Оплата:</b> переводом на \u203C\uFE0F {} \u203C\uFE0F по номеру {}, "
                           "только после забора биоматериала!".format(bank, phone))
        if delivery == "самообращение":
            address = job_db.execute("""SELECT address FROM services WHERE city = ?""", (city,)).fetchone()[0]
        if back_to_setting_analyses in "{}".format(id_date):
            confirm_order = confirm
            message_text_setting_orders = (f"\U0001F4C6<b>Дата:</b> {id_date.split('>>')[0]} (+/- 25 мин)"
                                           f"\n\U0000267B <b>{name}</b>"
                                           f"\n-----------------------------------"
                                           f"\n\U0001F9EA <b>Анализы:</b>"
                                           f"\n{analysis}"
                                           f"\n-----------------------------------"
                                           f"\n\U0001F4B5 <b>Сумма:</b> {price} \u20BD"
                                           f"\n-----------------------------------"
                                           f"\n\U0001F307 <b>Город:</b> {city}, {delivery} "
                                           f"\n\u27A1<b>по адресу:</b> {address}"
                                           f"\n-----------------------------------"
                                           f"\n\U0001F4AC <b>Комментарии:</b> {comm}"
                                           f"\n-----------------------------------"
                                           f"\n\U0001F4C6<b>Дата:</b> {id_date.split('>>')[0]} (+/- 25 мин)"
                                           f"\n-----------------------------------")
            date = id_date
            transfer_date = id_date

    if confirm_order == "не подтверждена":
        emoji_str = "\U0000274C"
    else:
        emoji_str = "\u2705"
    # =======================================================================================================
    id_midwifery = basket_db.execute(f"""SELECT id_midwifery FROM user_{user_id} WHERE id_date = ?""",
                                     (transfer_date,)).fetchone()[0]
    midwifery_db.execute("""SELECT * FROM users_midwifery WHERE user_id = ?""", (id_midwifery,))
    found_midwifery = midwifery_db.fetchall()
    message_text = ""
    for i, (user, name, female, patronymic, phone, city_in_mid) in enumerate(found_midwifery, start=1):
        message_text = (f"\n<b>Мед.сестра:</b> {name} {patronymic} "
                        f"\n\U0000260E: {phone} "
                        f"\n<b>=======================</b>"
                        f"\n\U0000267B<b>Статус заявки:</b>  {confirm_order}  {emoji_str}")
    message_text_setting_orders += message_text
    # =======================================================================================================
    message_text_setting_orders += cash_phone_bank

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    pay = types.InlineKeyboardButton("выполнено \U000023E9", callback_data=f"inArchive_{date}")
    delete = types.InlineKeyboardButton("отменить \U00002702 \U0000FE0F",
                                        callback_data=f"delOrder-{date}_{id_midwifery}")
    setting_orders_then_config = types.InlineKeyboardButton("изменить \U0001F6E0",
                                                            callback_data=f"setting_orders_then_config_{date}")
    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="back_to_orders")
    keyboard.add(pay, delete, setting_orders_then_config, back)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=message_text_setting_orders, reply_markup=keyboard)


# TODO ==========================================================================================================
# TODO КНОПКА УДАЛИТЬ ЗАЯВКУ
@router.callback_query_handler(lambda c: c.data.startswith("delOrder-"))
async def process_delete_orders(call: types.CallbackQuery):
    global date_add_collection_back
    date = call.data.split("delOrder-")[1]
    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="back_to_orders")
    delete_all_order = types.InlineKeyboardButton("отменить \U00002702 \U0000FE0F",
                                                  callback_data=f"delAllOrder_{date}")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(delete_all_order, back)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="\U0000203C️ \U0000FE0F Будет удалена вся информация и результаты "
                                     "данной заявки! Передайте в архив заявку для сохранения результатов!"
                                     "\n\U0000203C️ \U0000FE0F Загруженные результаты в чат-боте сохраняются!",
                                reply_markup=keyboard)


# TODO ==========================================================================================================
# TODO КНОПКА УДАЛИТЬ ЗАЯВКУ
@router.callback_query_handler(lambda c: c.data.startswith("delAllOrder_"))
async def process_delete_all_orders(call: types.CallbackQuery):
    user_id = call.message.chat.id

    date = call.data.split("delAllOrder_")[1]
    del_date = date.split("_")[0]
    print(date)

    # TODO Удаляем подтвержденную заявку
    basket_db.execute(f"DELETE FROM user_{user_id} WHERE id_date = ?", (del_date,))
    conn_basket.commit()

    # TODO восстанавливаем дату в БД у фельдшеров

    # TODO добавляем в БД фельдшера выбранную дату со значком "галочка"
    date_add_db.execute(f"""UPDATE nurse SET done = ? WHERE date = ?""", ("\U0001F4CC", date))
    midwifery_conn.commit()

    # TODO удаляем запись с БД (order_done) фельдшеров
    order_done_db.execute(f"DELETE FROM user_{date.split('_')[1]} WHERE id_date = ?", (del_date,))
    connect_order_done.commit()

    # TODO удаляем запись с БД profit_income_db
    profit_income_db.execute("DELETE FROM users WHERE date = ?", (del_date,))
    connect_profit_income.commit()

    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="back_to_orders")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(back)

    # try:
    #     # Удаляем каталог и его содержимое
    #     shutil.rmtree(folder_path_date)
    #     print("3735 Каталог удален успешно!")
    # except OSError as error:
    #     print(f"3737 Не удалось удалить каталог: {error}")

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="\U00002702 \U0000FE0F Удалено!", reply_markup=keyboard)


# TODO =============================================================================================================
# TODO ============================  РЕДАКТИРОВАТЬ ЗАЯВКУ ПОСЛЕ ЕГО ПОДТВЕРЖДЕНИЕ    ===============================
# TODO =============================================================================================================
@router.callback_query_handler(lambda c: c.data.startswith("setting_orders_then_config_"))
async def process_setting_orders_then_config(call: types.CallbackQuery):
    global message_text_setting_orders
    date = call.data.split("setting_orders_then_config_")[1]

    button_analysis = types.InlineKeyboardButton("сохранить шаблон \U0001F4BE", callback_data=f"savePattern_{date}")
    transfer_orders = types.InlineKeyboardButton("как перенести заявку \U0001F500 \U0001F558",
                                                 callback_data=f"transferOrders_{date}")
    back_to_confirm_orders = types.InlineKeyboardButton("назад \U000023EA", callback_data=f"ordersShow_{date}")
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(button_analysis,
                                                           transfer_orders, back_to_confirm_orders)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=message_text_setting_orders, reply_markup=keyboard)


# TODO ============================  ДОБАВИТЬ ИЛИ УДАЛИТЬ АНАЛИЗЫ ПОСЛЕ ИХ ПОДТВЕРЖДЕНИЕ    ========================
@router.callback_query_handler(lambda c: c.data.startswith("savePattern_"))
async def process_save_pattern(call: types.CallbackQuery):
    global transfer_date, result_numbers
    date = call.data.split("savePattern_")[1]
    user_id = call.message.chat.id
    # В этом разделе поставлена задача добавить в список анализов. Получает порядковый номер анализов которых
    # ранее выбрали и выводим в консоль эти анализы, далее предлагаем поиск
    dict_analysis = basket_db.execute(f"""SELECT analysis FROM user_{user_id} WHERE id_date = ?""",
                                      (transfer_date,)).fetchone()
    summ_cash = 0
    # этот список анализов полученное из БД созданного заказа
    analysis_list = dict_analysis[0].split('\n')
    # разделяем полученный анализ по кодам
    for analysis in analysis_list:
        analysis_parts = analysis.split('>>')[0]
        result_numbers.append(analysis_parts)

    all_analysis_db.execute("""SELECT * FROM clinic""")
    result = all_analysis_db.fetchall()
    for i, (sequence, id_list, name_analysis, price, info, tube, readiness, sale, sale_number,
            price_other, *any_column) in enumerate(result, start=1):
        if str(sequence) in result_numbers:
            summ_cash += price

    button_analysis = types.InlineKeyboardButton("сохранить \U0001F4BE", callback_data="get_to_analysis")
    back_to_confirm_orders = types.InlineKeyboardButton("назад \U000023EA",
                                                        callback_data=f"setting_orders_then_config_{date}")
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(button_analysis, back_to_confirm_orders)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"\U0001F4DD <b>Список анализов:</b> "
                                     f"\n{dict_analysis[0]}"
                                     f"\n<b>==============================</b>"
                                     f"\n\U0001F4B5<b>Сумма:</b> {summ_cash} \U000020BD"
                                     f"\n<b>==============================</b>"
                                     f"\n\u203CПри сохранении, в шаблоне остаются только списки анализов! Их можно "
                                     f"оформить при создании новой заявки в разделе >>>  \U0001F6D2 Корзина",
                                reply_markup=keyboard)


# TODO ============================  ПОИСК АНАЛИЗОВ ПОСЛЕ ПОДТВЕРЖДЕНИЯ ЗАЯВКИ    ========================
@router.callback_query_handler(lambda c: c.data == "get_to_analysis")
async def process_save_pattern_after(call: types.CallbackQuery):
    global last_bot_message_id, transfer_date
    sent_message = await bot.send_message(chat_id=call.message.chat.id, text="Введите название шаблона: ")
    last_bot_message_id = sent_message.message_id
    await States.waiting_for_save_pattern_name.set()


# =====сохраняем шаблон
@router.message_handler(state=States.waiting_for_save_pattern_name)
async def process_save_pattern_after_confirm(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    global last_bot_message_id, result_numbers
    input_text = message.text
    str_numbers_for_save_analysis = ", ".join(result_numbers)

    pattern_db.execute(f"""INSERT OR IGNORE INTO user_{user_id} (date, name_pattern, analysis_numbers) 
    VALUES (?, ?, ?)""", (transfer_date, input_text, str_numbers_for_save_analysis))
    connect_pattern.commit()
    if isinstance(last_bot_message_id, int):
        await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text="\u2705 Шаблон сохранен! ")
    result_numbers.clear()
    await state.finish()


# TODO =======================================================================================================
@router.callback_query_handler(lambda c: c.data.startswith("transferOrders_"))
async def process_transfer_orders(call: types.CallbackQuery):
    date = call.data.split("transferOrders_")[1]
    back_to_confirm_orders = types.InlineKeyboardButton("назад \U000023EA",
                                                        callback_data=f"setting_orders_then_config_{date}")
    basket_menu_button = types.InlineKeyboardButton("\U0001F6D2 Корзина", callback_data="back_to_basket_menu")
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(basket_menu_button, back_to_confirm_orders)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"\n\u203CВНИМАТЕЛЬНО"
                                     f"\n1) Сохраните шаблон"
                                     f"\n2) Перейдите в >>>\U0001F6D2 Корзина"
                                     f"\n3) Оформите заявку с новой датой",
                                reply_markup=keyboard)


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1 = > КОМУ ЗАКАЗАТЬ?
#           8.1.1 = > КНОПКА "МНЕ" - готово!
#   8.2 = > КНОПКА "ВЫБРАТЬ ДАТУ ЗАКАЗА"
#           8.1.32 = > КНОПКА "НАЗАД В КОРЗИНУ" - готово!
#           8.1.33 = > КНОПКА "СЛЕДУЮЩИЙ МЕСЯЦ"
#                8.1.33.1 = > КНОПКА "НАЗАД" в предыдущий месяц - готово!
#   8.3 = > В АРХИВ
#
# ==========================================================================================================
@router.callback_query_handler(lambda c: c.data.startswith("inArchive_"))
async def process_archive_the_order(call: types.CallbackQuery):
    date = call.data.split("inArchive_")[1]
    user_id = call.message.chat.id
    archive_db.execute(
        f"""CREATE TABLE IF NOT EXISTS user_{user_id} (
        id_date TEXT,
        name TEXT,
        analysis TEXT,
        price INTEGER,
        address TEXT,
        city TEXT,
        delivery TEXT,
        comment TEXT,
        confirm TEXT,
        id_midwifery TEXT
        )""")
    connect_archive.commit()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="back_to_orders")
    keyboard.add(back)

    # TODO ========================================================================================================
    # TODO выводим данные из БД basket.db готовую заявку из таблицы user_{user_id}
    basket_db.execute(f"""SELECT * FROM user_{user_id} WHERE id_date = ?""", (date,))
    basket = basket_db.fetchall()

    # TODO добавляем данные из готовой заявки в архивную БД archive.db
    for i, (date, name, analysis, price, address, city, delivery, comm, id_midwifery,
            confirm) in enumerate(basket, start=1):
        # TODO инициализируем ДБ архива учитывая новую дату
        archive_db.execute(f"""INSERT OR IGNORE INTO user_{user_id} (id_date, name, analysis, price, address, city, 
            delivery, comment, confirm, id_midwifery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (date, name, analysis, price, address, city, delivery, comm, confirm, id_midwifery))
        connect_archive.commit()
        # archive_db.execute(f"""UPDATE user_{user_id} SET id_date = ?, name = ?, analysis = ?,
        #                 price = ?, address = ?, city = ?, delivery = ?, comment = ?, confirm =?, id_midwifery = ?""",
        #                    (date, name, analysis, price, address, city, delivery,
        #                     comm, confirm, id_midwifery))
        # connect_archive.commit()

    # TODO удаляем данные из БД basket.db  таблицы user_{user_id}
    basket_db.execute(f"""DELETE FROM user_{user_id} WHERE id_date = ?""", (date,))
    conn_basket.commit()

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="\U0001F4C7 добавлен в архив", reply_markup=keyboard)
