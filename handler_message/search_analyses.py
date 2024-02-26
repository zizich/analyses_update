import aiogram
from aiogram import Router, F, exceptions
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.any_process import translate_any_number_analysis
from core.fsm_engine import States
from core.search_algorithm import search_analyses
from data_base import cursor_db, basket_db, conn_basket, sur_analysis_db, all_analysis_db

router = Router(name=__name__)

search_word = ""  # переменная для назначения анализа, она нужна для кнопки назад, при нажатии которого переходит


@router.message(F.data.in_(['\U0001F489 Анализы']))
async def process_take_tests(message: Message):
    user_id = message.chat.id
    basket_db.execute("""INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (user_id, None, None, None, None, None, None, None, None, None, None, None))
    conn_basket.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Комплексы \U0001F9EA", callback_data="group_buttons")
    keyboard.button(text="Поиск \U0001F50E", callback_data="search_analysis")
    keyboard.button(text="Стоп лист \u26D4\ufe0f", callback_data="stop_list")
    keyboard.adjust(1)
    await message.answer(text="\U000027A1 Перед выбором, ознакомьтесь со стоп-листом \U0001F6AB: ",
                         reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data == "back_to_analyses")
async def process_back_to_analyses(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Комплексы \U0001F9EA", callback_data="group_buttons")
    keyboard.button(text="Поиск \U0001F50E", callback_data="search_analysis")
    keyboard.button(text="Стоп лист \u26D4\ufe0f", callback_data="stop_list")
    keyboard.adjust(1)
    await call.message.answer(text="\U000027A1 Перед выбором, ознакомьтесь со стоп-листом \U0001F6AB: ",
                              reply_markup=keyboard.as_markup())


# ==========================================================================================================
#                                       ПОИСК АНАЛИЗОВ:
# ==========================================================================================================
@router.callback_query(lambda c: c.data == "search_analysis")
async def process_go_to_search_analysis(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_search)
    await call.message.answer(chat_id=call.message.chat.id,
                              text="\U000026A0 ВНИМАНИЕ \U0000203C"
                                   "\n=================="
                                   "\n При поиске анализа: "
                                   "\n\U00002757 Пишите полное/короткое наименование анализа"
                                   "\n\U00002757 Пишите с Заглавными буквами либо АББРЕВИАТУРУ!"
                                   "\n\U00002757 Пишите Английское наименование анализа!"
                                   "\n================== \nВведите наименование анализа: ")


@router.message(States.waiting_for_search)
async def process_find_search(message: Message, state: FSMContext):
    user_id = message.chat.id
    await state.clear()
    global search_word

    try:
        # логика такова: сначала проверяется корзина, выбран ли там город, если город не выбран, то поиск анализов
        # осуществляется по городу выбранной при регистрации, иначе берется город из корзины
        try:
            city = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
            if city is None:
                city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        except TypeError:
            city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

        search_word = message.text
        keyboard = search_analyses(message.text, city)
        keyboard.button(text="поиск \U0001F50E", callback_data="search_analysis")
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
        keyboard.adjust(1)

        await message.answer(text="\U0000267B Поиск завершен", reply_markup=keyboard.as_markup())
    except exceptions.TelegramBadRequest:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="поиск \U0001F50E", callback_data="search_analysis")
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
        keyboard.adjust(1)
        await message.answer(text="\U0000203C️ \U0000FE0F Список найденных анализов под Ваш запрос превышает лимит и "
                                  "не вмещается в одно сообщение! \nПожалуйста, повторите поиск и напишите "
                                  "наименование анализа более подробно",
                             reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data.startswith('id_'))
async def process_income_analysis(call: CallbackQuery):
    idAnalyses = (call.data.split('id_')[1]).split("-")[0]
    city = (call.data.split('id_')[1]).split("-")[1]

    if city in "Сургут":
        stop_analysis = sur_analysis_db.execute("""SELECT stopped FROM clinic WHERE id_num = ?""",
                                                (idAnalyses,)).fetchone()[0]
        all_analyses = sur_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,))
    else:
        stop_analysis = all_analysis_db.execute("""SELECT stopped FROM clinic WHERE id_num = ?""",
                                                (idAnalyses,)).fetchone()[0]
        all_analyses = all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,))

    name_analysis = ""
    if stop_analysis == 1:
        for i, (id_num, id_list, analysis, price, info, tube, readiness, sale, sale_number, price_other, stopped) in (
                enumerate(all_analyses.fetchall(), start=1)):
            name_analysis = ("<b>{}</b>\n===========================\nЦена: {}\u20BD "
                             "\nСрок готовности: {} дн.").format(analysis.split('(')[0], price, readiness)

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text=f"поиск \U0001F50E", callback_data="search_analysis")
        keyboard.button(text="добавить \U00002705", callback_data=f"addAn_{idAnalyses}-{city}")
        keyboard.button(text="информация \U00002753", callback_data=f"infoAn_{idAnalyses}-{city}")
        keyboard.button(text="удалить \U0000274E", callback_data=f"delAn_{idAnalyses}-{city}")
        keyboard.button(text="назад \U000023EA", callback_data="back_to_previous_search")
        keyboard.adjust(2)
        await call.message.answer(text=name_analysis, reply_markup=keyboard.as_markup())
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="назад \U000023EA", callback_data="back_to_previous_search")
        keyboard.adjust(1)
        await call.message.answer(text="\U0000203C Анализ на СТОП ЛИСТЕ \U0001F6AB: "
                                       "\n=========================="
                                       "\n" + translate_any_number_analysis(call.data),
                                  reply_markup=keyboard.as_markup())


@router.callback_query(lambda c: c.data == "back_to_previous_search")
async def previous_search(call: CallbackQuery):
    user_id = call.message.chat.id
    global search_word

    try:
        # логика такова: сначала проверяется корзина, выбран ли там город, если город не выбран, то поиск анализов
        # осуществляется по городу выбранной при регистрации, иначе берется город из корзины

        try:
            city = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
            if city is None:
                city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        except TypeError:
            city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

        keyboard = search_analyses(search_word, city)
        keyboard.button(text="поиск \U0001F50E", callback_data="search_analysis")
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
        keyboard.adjust(1)

        await call.message.answer(text="\U0000267B Поиск завершен", reply_markup=keyboard)
    except exceptions.TelegramBadRequest:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        back_to_search = types.InlineKeyboardButton("поиск \U0001F50E", callback_data="search_analysis")
        back = types.InlineKeyboardButton("назад \U000023EA", callback_data="back_to_analyses")
        keyboard.add(back_to_search, back)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="\U0000267B Список найденных анализов под Ваш запрос "
                                         "превышает лимит и не вмещается в одно сообщение!"
                                         + "\nПожалуйста, повторите поиск и напишите наименование "
                                           "анализа более подробно.",
                                    reply_markup=keyboard)


# ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (ДОБАВИТЬ)
@router.callback_query_handler(lambda c: c.data.startswith('addAn_'))
async def processing_found_analysis_search(call: types.CallbackQuery):
    user_id = call.message.chat.id
    idAnalyses = (call.data.split('addAn_')[1]).split("-")[0]
    city = (call.data.split('addAn_')[1]).split("-")[1]

    if city in "Сургут":
        result = sur_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,)).fetchall()
    else:
        result = all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,)).fetchall()

    text_for_added = ""
    for i, (id_analysis, id_list, name_analysis, price, info, tube, readiness, sale,
            sale_number, price_other, stop) in enumerate(result, start=1):
        add_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                       (id_analysis, name_analysis.split('(')[0], price, tube, readiness))
        connect_added.commit()

        price_income = price - price_other
        profit_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                          (id_analysis, name_analysis.split('(')[0], price, price_other, price_income))
        connect_profit.commit()
        text_for_added = (f"{name_analysis.split('(')[0]}"
                          "\n==========================="
                          "\n\U00002705 Добавлено в КОРЗИНУ!")

    keyboard_added = types.InlineKeyboardMarkup()
    back_to_search_button = types.InlineKeyboardButton("\U0001F50E поиск ", callback_data="search_analysis")
    back_found_analysis = types.InlineKeyboardButton("назад \U000023EA",
                                                     callback_data=f"back_to_previous_search")
    basket_menu_button = types.InlineKeyboardButton("\U0001F4E5 корзина", callback_data="back_to_basket_menu")
    keyboard_added.add(back_to_search_button).add(basket_menu_button).add(back_found_analysis)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text_for_added, reply_markup=keyboard_added)


# ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (ИНФО)
@router.callback_query_handler(lambda c: c.data.startswith('infoAn_'))
async def processing_found_analysis_info(call: types.CallbackQuery):
    idAnalyses = (call.data.split('infoAn_')[1]).split("-")[0]
    city = (call.data.split('infoAn_')[1]).split("-")[1]

    if city in "Сургут":
        result = sur_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,)).fetchall()
    else:
        result = all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,)).fetchall()

    outcome = ""
    for i, (id_analysis, id_list, name_analysis, price, info, tube, readiness, sale,
            sale_number, price_other, stop) in enumerate(result, start=1):
        outcome = ("\U0000203C " + info + "\n==================" + "\nЦена: {}\u20BD".format(price)
                   + "\nСрок готовности через: {} дн.".format(readiness))

    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("\U0001F50E поиск ", callback_data="search_analysis")
    back_to_found_analysis = types.InlineKeyboardButton("назад \U000023EA",
                                                        callback_data=f"id_{idAnalyses}")
    basket = types.InlineKeyboardButton("\U0001F4E5 корзина", callback_data="back_to_basket_menu")
    keyboard.add(back).add(basket).add(back_to_found_analysis)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=outcome, reply_markup=keyboard)


# TODO  ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (УДАЛИТЬ)
@router.callback_query_handler(lambda c: c.data.startswith('delAn_'))
async def processing_found_analysis_delete(call: types.CallbackQuery):
    user_id = call.message.chat.id
    idAnalyses = (call.data.split('delAn_')[1]).split("-")[0]
    city = (call.data.split('delAn_')[1]).split("-")[1]

    if city in "Сургут":
        name_analysis = sur_analysis_db.execute("""SELECT name_analysis FROM clinic WHERE id_num = ?""",
                                                (idAnalyses,)).fetchone()[0]
    else:
        name_analysis = all_analysis_db.execute("""SELECT name_analysis FROM clinic WHERE id_num = ?""",
                                                (idAnalyses,)).fetchone()[0]

    add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (idAnalyses,))
    connect_added.commit()

    profit_db.execute(f"DELETE FROM user_{user_id} WHERE id_list = ?", (idAnalyses,))
    connect_profit.commit()

    outcome = "Анализ: " + f"\n{name_analysis.split('(')[0]}" + "\n \U0000274E  удален из корзины!"

    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("\U0001F50E поиск ", callback_data="search_analysis")
    back_to_found_analysis = types.InlineKeyboardButton("назад \U000023EA",
                                                        callback_data="back_to_previous_search")
    basket = types.InlineKeyboardButton("\U0001F4E5 корзина", callback_data="back_to_basket_menu")
    keyboard.add(back).add(basket).add(back_to_found_analysis)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=outcome, reply_markup=keyboard)


# ==========================================================================================================
#                                       КОМПЛЕКСЫ АНАЛИЗОВ:
# ==========================================================================================================
@router.callback_query_handler(lambda c: c.data == "group_buttons")
async def process_go_to_group_analysis(call: types.CallbackQuery):
    # TODO выводим из БД список всех анализов и их параметров. Итерируем анализы по полученной группе (сортировка по
    # TODO - уникальному номеру каждого анализа

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="back_to_analyses")

    all_complex_out = complex_analyses_db.execute("""SELECT * FROM complex""").fetchall()

    try:
        collection_buttons = []
        for i, (name_rus, name_eng, numbers) in enumerate(all_complex_out, start=1):
            button = types.InlineKeyboardButton(f"{name_rus}", callback_data=f"group_{name_eng}")
            collection_buttons.append(button)

        keyboard.add(*collection_buttons)
        keyboard.add(back)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Комплексы анализов \U0001F5C4:",
                                    reply_markup=keyboard)
    except TypeError:
        keyboard.add(back)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Комплексов нет! \U0001F5C4:",
                                    reply_markup=keyboard)


# TODO  ОБРАБОТКА КНОПКИ ВЫБОРА КОМПЛЕКСА
@router.callback_query_handler(lambda c: c.data.startswith("group_"))
async def process_complex_watch(call: types.CallbackQuery):
    user_id = call.message.chat.id
    global list_sequence
    try:
        try:
            city = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
            if city is None:
                city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        except TypeError:
            city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

        text_output = all_complex(call.data.split('group_')[1], city)
        list_sequence = all_complex_selected(call.data.split('group_')[1])

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        add_selected = types.InlineKeyboardButton("добавить", callback_data=f"addSlctd_{city}")
        delete_selected = types.InlineKeyboardButton("удалить", callback_data=f"delSlctd_{city}")
        back = types.InlineKeyboardButton("назад \U000023EA", callback_data="group_buttons")
        keyboard.add(add_selected, delete_selected, back)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text_output,
                                    reply_markup=keyboard)
    except (AttributeError, IndexError, TypeError):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        back = types.InlineKeyboardButton("назад \U000023EA", callback_data="group_buttons")
        keyboard.add(back)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="\u203C Комплекс в стадии формирования....Попробуйте позже!",
                                    reply_markup=keyboard)


# TODO ОБРАБОТКА КНОПКИ "ДОБАВИТЬ" ВЫБРАННОГО КОМПЛЕКСА
@router.callback_query_handler(lambda c: c.data.startswith("addSlctd_"))
async def process_komplex_add(call: types.CallbackQuery):
    user_id = call.message.chat.id
    global list_sequence
    # ======================================================================================================
    city = call.data.split('addSlctd_')[1]

    if city in "Сургут":
        sur_analysis_db.execute("""SELECT * FROM clinic""")
        result = all_analysis_db.fetchall()
    else:
        all_analysis_db.execute("""SELECT * FROM clinic""")
        result = all_analysis_db.fetchall()
    # ======================================================================================================
    outcome = ""
    for i, (id_analysis, id_list, name_analysis, price, info, tube, readiness, sale, sale_number,
            price_other, *any_column) in enumerate(result, start=1):
        if id_analysis in map(int, list_sequence):
            add_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                           (id_analysis, name_analysis, price, tube, readiness))
            connect_added.commit()
            outcome = "\U00002705 Добавлено в Корзину!"

            price_income = price - price_other
            profit_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                              (id_list, name_analysis, price, price_other, price_income))
            connect_profit.commit()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="group_buttons")
    basket = types.InlineKeyboardButton("корзина \U0001F4E5", callback_data="back_to_basket_menu")
    keyboard.add(basket, back)
    list_sequence.clear()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=outcome,
                                reply_markup=keyboard)


@router.callback_query_handler(lambda c: c.data.startswith("delSlctd_"))
async def process_komplex_add(call: types.CallbackQuery):
    user_id = call.message.chat.id
    global list_sequence
    # ======================================================================================================
    city = call.data.split('delSlctd_')[1]

    if city in "Сургут":
        sur_analysis_db.execute("""SELECT * FROM clinic""")
        result = all_analysis_db.fetchall()
    else:
        all_analysis_db.execute("""SELECT * FROM clinic""")
        result = all_analysis_db.fetchall()
    # ======================================================================================================
    outcome = ""
    for i, (id_analysis, id_list, name_analysis, price, info, tube, readiness, sale, sale_number,
            price_other, *any_column) in enumerate(result, start=1):
        if id_analysis in map(int, list_sequence):
            add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (id_analysis,))
            connect_added.commit()
            outcome = "Удален из Корзины!"

            profit_db.execute(f"DELETE FROM user_{user_id} WHERE id_list = ?", (id_list,))
            connect_profit.commit()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton("назад \U000023EA", callback_data="group_buttons")
    basket = types.InlineKeyboardButton("корзина \U0001F4E5", callback_data="back_to_basket_menu")
    keyboard.add(basket, back)
    list_sequence.clear()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=outcome,
                                reply_markup=keyboard)


# ОБРАБОТКА КНОПКИ СТОП-ЛИСТА
@router.callback_query_handler(lambda c: c.data == "stop_list")
async def process_stop_list(call: types.CallbackQuery):
    user_id = call.message.chat.id
    try:
        city = basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
        if city is None:
            city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
    except TypeError:
        city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    stop_analyses = []
    if city in "Сургут":
        sur_analysis_db.execute("""SELECT * FROM clinic WHERE stopped = ?""", (0,))
        result = all_analysis_db.fetchall()
    else:
        all_analysis_db.execute("""SELECT * FROM clinic WHERE stopped = ?""", (0,))
        result = all_analysis_db.fetchall()
    for i, (num, id_list, name, *other) in enumerate(result, start=1):
        stop_set = f"{i}) {name}"
        stop_analyses.append(stop_set)

    message_stop = "\n".join(stop_analyses)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton("назад", callback_data="back_to_analyses")
    keyboard.add(back)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=message_stop + "\n======================="
                                                    "\n\u203C\uFE0FАнализы свыше находятся в стоп-листе! "
                                                    "\n\u203C\uFE0FСкоро запустим их!",
                                reply_markup=keyboard)
