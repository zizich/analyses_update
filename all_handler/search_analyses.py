from aiogram import Router, F, exceptions
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.any_process import translate_any_number_analysis
from core.fsm_engine import States
from core.search_algorithm import search_analyses, all_complex, all_complex_selected
from data_base import basket_db, conn_basket, all_analysis_db, add_db, connect_added, \
    profit_db, connect_profit, complex_analyses_db
from keyboard import base_menu_analyses, info_by_analyses, kb_previous_search, kb_search_analyses_after_done, kb_complex

router = Router(name=__name__)

search_word = ""  # переменная для назначения анализа, она нужна для кнопки назад, при нажатии которого переходит


@router.message(F.text.in_(['\U0001F489 Анализы']))
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


@router.callback_query(F.data == "back_to_analyses")
async def process_back_to_analyses(call: CallbackQuery):
    await call.message.edit_text(text="\U000027A1 Перед выбором, ознакомьтесь со стоп-листом \U0001F6AB: ",
                                 reply_markup=await base_menu_analyses())


# ==========================================================================================================
#                                       ПОИСК АНАЛИЗОВ:
# ==========================================================================================================
@router.callback_query(F.data == "search_analysis")
async def process_go_to_search_analysis(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_search)
    await call.message.edit_text(text="\U000026A0 ВНИМАНИЕ \U0000203C"
                                      "\n=================="
                                      "\n При поиске анализа: "
                                      "\n\U00002757 Пишите полное/короткое наименование анализа"
                                      "\n\U00002757 Пишите с Заглавными буквами либо АББРЕВИАТУРУ!"
                                      "\n\U00002757 Пишите Английское наименование анализа!"
                                      "\n================== \nВведите наименование анализа: ")


@router.message(States.waiting_for_search)
async def process_find_search(message: Message, state: FSMContext):
    await state.clear()
    global search_word

    try:
        search_word = message.text
        keyboard = search_analyses(message.text)
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


@router.callback_query(F.data.startswith('id_'))
async def process_income_analysis(call: CallbackQuery):
    idAnalyses = (call.data.split('id_')[1]).split("-")[0]
    stop_analysis = all_analysis_db.execute("""SELECT stopped FROM clinic WHERE id_num = ?""",
                                            (idAnalyses,)).fetchone()[0]
    all_analyses = all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,))

    name_analysis = ""
    if stop_analysis == 1:
        for i, (id_num, id_list, analysis, price, info, tube, readiness, sale, sale_number, price_other, stopped) in (
                enumerate(all_analyses.fetchall(), start=1)):
            name_analysis = ("<b>{}</b>\n===========================\nЦена: {}\u20BD "
                             "\nСрок готовности: {} дн.").format(analysis.split('(')[0], price, readiness)

        await call.message.edit_text(text=name_analysis, reply_markup=await info_by_analyses(idAnalyses))
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="назад \U000023EA", callback_data="back_to_previous_search")
        keyboard.adjust(1)
        await call.message.answer(text="\U0000203C Анализ на СТОП ЛИСТЕ \U0001F6AB: "
                                       "\n=========================="
                                       "\n" + translate_any_number_analysis(call.data),
                                  reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "back_to_previous_search")
async def previous_search(call: CallbackQuery):
    try:
        # логика такова: сначала проверяется корзина, выбран ли там город, если город не выбран, то поиск анализов
        # осуществляется по городу выбранной при регистрации, иначе берется город из корзины

        async def search_kb():
            global search_word
            kb_previous = search_analyses(search_word)
            kb_previous.add(InlineKeyboardButton(text="поиск \U0001F50E", callback_data="search_analysis"))
            kb_previous.add(InlineKeyboardButton(text="корзина \U0001F4E5", callback_data="back_to_basket_menu"))
            kb_previous.add(InlineKeyboardButton(text="назад \U000023EA", callback_data="back_to_analyses"))
            kb_previous.adjust(1)
            return kb_previous.as_markup()

        await call.message.edit_text(text="\U0000267B Поиск завершен",
                                     reply_markup=await search_kb())
    except exceptions.TelegramBadRequest:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="поиск \U0001F50E", callback_data="search_analysis")
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
        await call.message.answer(text="\U0000267B Список найденных анализов под Ваш запрос "
                                       "превышает лимит и не вмещается в одно сообщение!"
                                       + "\nПожалуйста, повторите поиск и напишите наименование "
                                         "анализа более подробно.",
                                  reply_markup=keyboard.adjust(1).as_markup())


# ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (ДОБАВИТЬ)
@router.callback_query(F.data.startswith('addAn_'))
async def processing_found_analysis_search(call: CallbackQuery):
    user_id = call.message.chat.id
    idAnalyses = (call.data.split('addAn_')[1]).split("-")[0]

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

    await call.message.edit_text(text=text_for_added, reply_markup=await kb_previous_search())


# ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (ИНФО)
@router.callback_query(F.data.startswith('infoAn_'))
async def processing_found_analysis_info(call: CallbackQuery):
    idAnalyses = (call.data.split('infoAn_')[1]).split("-")[0]

    result = all_analysis_db.execute("""SELECT * FROM clinic WHERE id_num = ?""", (idAnalyses,)).fetchall()

    outcome = ""
    for i, (id_analysis, id_list, name_analysis, price, info, tube, readiness, sale,
            sale_number, price_other, stop) in enumerate(result, start=1):
        outcome = ("\U0000203C " + info + "\n==================" + "\nЦена: {}\u20BD".format(price)
                   + "\nСрок готовности через: {} дн.".format(readiness))

    async def inline_kb():
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="\U0001F50E поиск ", callback_data="search_analysis"))
        keyboard.add(InlineKeyboardButton(text="\U0001F4E5 корзина", callback_data="back_to_basket_menu"))
        keyboard.add(InlineKeyboardButton(text="назад \U000023EA", callback_data=f"id_{idAnalyses}"))
        keyboard.adjust(1)

        return keyboard.as_markup()

    await call.message.edit_text(text=outcome, reply_markup=await inline_kb())


# ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (УДАЛИТЬ)
@router.callback_query(F.data.startswith('delAn_'))
async def processing_found_analysis_delete(call: CallbackQuery):
    user_id = call.message.chat.id
    idAnalyses = (call.data.split('delAn_')[1]).split("-")[0]

    name_analysis = all_analysis_db.execute("""SELECT name_analysis FROM clinic WHERE id_num = ?""",
                                            (idAnalyses,)).fetchone()[0]

    add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (idAnalyses,))
    connect_added.commit()

    profit_db.execute(f"DELETE FROM user_{user_id} WHERE id_list = ?", (idAnalyses,))
    connect_profit.commit()

    outcome = "Анализ: " + f"\n{name_analysis.split('(')[0]}" + "\n \U0000274E  удален из корзины!"

    await call.message.edit_text(text=outcome, reply_markup=await kb_previous_search())


# ==========================================================================================================
#                                       КОМПЛЕКСЫ АНАЛИЗОВ:
# ==========================================================================================================
@router.callback_query(F.data == "group_buttons")
async def process_go_to_group_analysis(call: CallbackQuery):
    # Выводим из БД список всех анализов и их параметров. Итерируем анализы по полученной группе (сортировка по
    # - уникальному номеру каждого анализа
    await call.message.edit_text(text="Комплексы анализов \U0001F5C4:",
                                 reply_markup=await kb_complex())


# ОБРАБОТКА КНОПКИ ВЫБОРА КОМПЛЕКСА
@router.callback_query(F.data.startswith("group_"))
async def process_complex_watch(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    try:
        name_eng = call.data.split('group_')[1]
        text_output = all_complex(call.data.split('group_')[1])

        async def kb_info_complex():
            keyboard.button(text="добавить", callback_data=f"addSlctd_{name_eng}")
            keyboard.button(text="удалить", callback_data=f"delSlctd_{name_eng}")
            keyboard.button(text="назад \U000023EA", callback_data="group_buttons")
            keyboard.adjust(2)
            return keyboard.as_markup()

        await call.message.edit_text(text=text_output, reply_markup=await kb_info_complex())
    except (AttributeError, IndexError, TypeError):

        keyboard.button(text="назад \U000023EA", callback_data="group_buttons")
        keyboard.adjust(1)

        await call.message.answer(text="\u203C Комплекс в стадии формирования....Попробуйте позже!",
                                  reply_markup=keyboard.as_markup())


# ОБРАБОТКА КНОПКИ "ДОБАВИТЬ" ВЫБРАННОГО КОМПЛЕКСА
@router.callback_query(F.data.startswith("addSlctd_"))
async def process_komplex_add(call: CallbackQuery):
    user_id = call.message.chat.id
    list_sequence = all_complex_selected(call.data.split('addSlctd_')[1])
    # ======================================================================================================
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

    async def kb_buttons_in():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="group_buttons")
        keyboard.adjust(1)
        return keyboard.as_markup()

    await call.message.edit_text(text=outcome, reply_markup=await kb_buttons_in())


@router.callback_query(F.data.startswith("delSlctd_"))
async def process_komplex_add(call: CallbackQuery):
    user_id = call.message.chat.id
    list_sequence = all_complex_selected(call.data.split('delSlctd_')[1])
    # ======================================================================================================
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

    async def kb_buttons_in():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="group_buttons")
        keyboard.adjust(1)
        return keyboard.as_markup()

    list_sequence.clear()
    await call.message.edit_text(text=outcome, reply_markup=await kb_buttons_in())


# ОБРАБОТКА КНОПКИ СТОП-ЛИСТА
@router.callback_query(F.data == "stop_list")
async def process_stop_list(call: CallbackQuery):
    stop_analyses = []
    all_analysis_db.execute("""SELECT * FROM clinic WHERE stopped = ?""", (0,))
    result = all_analysis_db.fetchall()
    for i, (num, id_list, name, *other) in enumerate(result, start=1):
        stop_set = f"{i}) {name}"
        stop_analyses.append(stop_set)

    message_stop = "\n".join(stop_analyses)

    async def kb_buttons_in():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="back_to_analyses")
        keyboard.adjust(1)
        return keyboard.as_markup()

    await call.message.edit_text(text=message_stop + "\n======================="
                                                     "\n\u203C\uFE0FАнализы свыше находятся в стоп-листе! "
                                                     "\n\u203C\uFE0FСкоро запустим их!",
                                 reply_markup=await kb_buttons_in())
