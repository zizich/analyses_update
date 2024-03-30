import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.base import basket_db, add_db, job_db, cursor_db, all_analysis_db, connect_added

router = Router(name=__name__)

transfer_sale = any


# ================================================================================================================
# ==============================================          АКЦИИ         ==========================================
# ================================================================================================================
@router.message(F.text.in_("\U0001F6CD Акции"))
async def process_sale(message: Message):
    user_id = message.chat.id

    try:
        city = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        if city is None:
            city = cursor_db.execute(f"""SELECT city FROM users_{user_id} WHERE user_id = ?""",
                                     (f"{user_id}-1",)).fetchone()[0]
    except TypeError:
        city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    sale_text = job_db.execute("""SELECT all_sale FROM services WHERE city = ?""", (city,)).fetchone()[0]

    all_analysis_db.execute("""SELECT * FROM clinic WHERE sale = ?""", ("yes",))
    result_sale = all_analysis_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (id_analyses, id_list, name, price, info, tube, readiness, sale, sale_number, price_other, stop) in (
            enumerate(result_sale, start=1)):
        if stop != 0:
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
        city = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        if city is None:
            city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
    except TypeError:
        city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    sale_text = job_db.execute("""SELECT all_sale FROM services WHERE city = ?""", (city,)).fetchone()[0]

    all_analysis_db.execute("""SELECT * FROM clinic WHERE sale = ?""", ("yes",))
    result_sale = all_analysis_db.fetchall()

    keyboard = InlineKeyboardBuilder()

    for i, (id_analyses, id_list, name, price, info, tube, readiness, sale, sale_number, price_other, stop) in (
            enumerate(result_sale, start=1)):
        keyboard.button(text=f"{sale_number} % \U00002198 {name} ",
                        callback_data="actionShow_{}-{}".format(id_analyses, sale_number))
    keyboard.adjust(1)

    await call.message.edit_text(text=sale_text, reply_markup=keyboard.as_markup())


# ОБРАБОТКА ВЫБОРА АКЦИИ
@router.callback_query(F.data.startswith("actionShow_"))
async def process_go_to_sale_analyses(call: CallbackQuery):
    global transfer_sale
    message_sale = ""
    transfer_sale = re.findall(r'\d+', call.data.split("actionShow_")[1])[0]

    all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (transfer_sale,))
    result = all_analysis_db.fetchall()

    for i, (id_analyses, id_list, name, price, info, tube, readiness, sale, sale_number, price_other, stop) in (
            enumerate(result, start=1)):
        summ = price - ((price * sale_number) / 100)
        message_sale = (f"{name}\n================== \nИнформация: {info} \n================== "
                        f"\nЦена: {price} \U000020BD"
                        f"\nЦена по акции: {summ} \U000020BD")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="добавить", callback_data="add_sale")
    keyboard.button(text="удалить", callback_data="delete_sale")
    keyboard.button(text="назад \U000023EE", callback_data="back_to_sale")
    keyboard.adjust(2)
    await call.message.edit_text(text=message_sale, reply_markup=keyboard.as_markup())


# ДОБАВИТЬ ИЛИ УДАЛИТЬ ВЫБРАННУЮ АКЦИЮ
@router.callback_query(F.data == ["add_sale", "delete_sale"])
async def process_go_to_sale_add_or_delete(call: CallbackQuery):
    global transfer_sale
    user_id = call.message.chat.id

    all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (transfer_sale,))
    result = all_analysis_db.fetchall()

    outcome = ""

    if call.data == "add_sale":
        for i, (id_analysis, id_list, name_analysis, price, info, tube, readiness, sale,
                sale_number, price_other, stop) in enumerate(result, start=1):
            price_all = price - ((price * sale_number) / 100)
            add_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                           (id_analysis, name_analysis, price_all, tube, readiness))
            connect_added.commit()
            outcome = "\U00002705 Добавлено в Корзину!"
    elif call.data == "delete_sale":
        add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (transfer_sale,))
        connect_added.commit()
        outcome = "Удален из Корзины!"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="назад \U000023EA", callback_data="back_to_sale")
    keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
    keyboard.adjust(2)
    await call.message.answer(text=outcome, reply_markup=keyboard.as_markup())
