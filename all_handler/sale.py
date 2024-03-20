from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_base import database_db, connect_database

router = Router(name=__name__)

transfer_code_analyses = any


# ================================================================================================================
# ==============================================          АКЦИИ         ==========================================
# ================================================================================================================
@router.message(F.text.in_("\U0001F6CD Акции"))
async def process_sale(message: Message):
    user_id = message.chat.id

    try:
        city = database_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        if city is None:
            city = database_db.execute(f"""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
    except TypeError:
        city = database_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    sale_text = database_db.execute("""SELECT all_sale FROM cities_payment WHERE city = ?""", (city,)).fetchone()[0]

    database_db.execute("""SELECT * FROM analyses""")
    result_sale = database_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (id_analyses, id_list, name, price, info, tube, readiness, sale, sale_number, price_other, stop) in (
            enumerate(result_sale, start=1)):
        if stop != 0 and sale:
            keyboard.button(text=f"{sale_number} % \U00002198 {name} ",
                            callback_data="actionShow_{}-{}".format(id_analyses, sale_number))

    keyboard.adjust(1)

    # await bot.send_message(chat_id=message.chat.id, text="\U0001F449 Выберите: ", reply_markup=keyboard)
    await message.answer(text=sale_text, reply_markup=keyboard.as_markup())


# ВЕРНУТСЯ К АКЦИЯМ
@router.callback_query(F.data == "back_to_sale")
async def process_back_to_sale(call: CallbackQuery):
    user_id = call.message.chat.id

    try:
        city = database_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        if city is None:
            city = database_db.execute(f"""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
    except TypeError:
        city = database_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    sale_text = database_db.execute("""SELECT all_sale FROM cities_payment WHERE city = ?""", (city,)).fetchone()[0]

    database_db.execute("""SELECT * FROM analyses""")
    result_sale = database_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price,
            prime_cost, stop, commplex) in enumerate(result_sale, start=1):
        if stop != 0 and sale:
            keyboard.button(text=f"{sale} % \U00002198 {analysis} ",
                            callback_data="actionShow_{}".format(code_number))

    keyboard.adjust(1)

    await call.message.edit_text(text=sale_text, reply_markup=keyboard.as_markup())


# ОБРАБОТКА ВЫБОРА АКЦИИ
@router.callback_query(F.data.startswith("actionShow_"))
async def process_go_to_sale_analyses(call: CallbackQuery):
    message_sale = ""
    code_analyses = call.data.split("actionShow_")[1]

    database_db.execute("""SELECT * FROM analyses WHERE code_analyses = ?""", (code_analyses,))
    result = database_db.fetchall()

    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price,
            prime_cost, stop, commplex) in enumerate(result, start=1):
        summ = price - ((price * sale) / 100)
        message_sale = (f"{analysis}\n================== \nИнформация: {info} \n================== "
                        f"\nЦена: {price} \U000020BD"
                        f"\nЦена по акции: {summ} \U000020BD")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="добавить", callback_data=f"addSale_{code_analyses}")
    keyboard.button(text="удалить", callback_data=f"delSale_{code_analyses}")
    keyboard.button(text="назад \U000023EE", callback_data="back_to_sale")
    keyboard.adjust(2)
    await call.message.edit_text(text=message_sale, reply_markup=keyboard.as_markup())


# ДОБАВИТЬ ИЛИ УДАЛИТЬ ВЫБРАННУЮ АКЦИЮ
@router.callback_query(F.data.startswith("delSale_"))
@router.callback_query(F.data.startswith("addSale_"))
async def process_go_to_sale_add_or_delete(call: CallbackQuery):
    user_id = call.message.chat.id

    outcome = ""

    if call.data.split("addSale_")[0] == "addSale_":
        code_analyses = call.data.split("addSale_")[1]
        database_db.execute("""SELECT * FROM analyses WHERE code_analyses = ?""", (code_analyses,))
        result = database_db.fetchall()

        for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price,
                prime_cost, stop, commplex) in enumerate(result, start=1):
            income = price - prime_cost
            database_db.execute(f"INSERT OR IGNORE INTO users_analyses_selected VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (code_number, analysis, tube, readiness, price, prime_cost, income, user_id))
            connect_database.commit()
            outcome = "\U00002705 Добавлено в Корзину!"
    elif call.data.split("delSale_")[0] == "delSale_":
        code_analyses = call.data.split("delSale_")[1]
        database_db.execute(f"DELETE FROM users_analyses_selected WHERE code_analyses = ?", (code_analyses,))
        connect_database.commit()
        outcome = "Удален из Корзины!"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад \U000023EA", callback_data="back_to_sale")
    keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
    keyboard.adjust(2)
    await call.message.answer(text=outcome, reply_markup=keyboard.as_markup())
