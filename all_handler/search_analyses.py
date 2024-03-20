from aiogram import Router, F, exceptions
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.any_process import translate_any_number_analysis
from core.fsm_engine import States
from core.search_algorithm import search_analyses, all_complex
from data_base import database_db, connect_database
from keyboard import base_menu_analyses, info_by_analyses, kb_previous_search, kb_complex

router = Router(name=__name__)

search_word = ""  # переменная для назначения анализа, она нужна для кнопки назад, при нажатии которого переходит


@router.message(F.text.in_(['\U0001F489 Анализы']))
async def process_take_tests(message: Message):
    user_id = message.chat.id
    database_db.execute("""INSERT OR IGNORE INTO users_selected VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (user_id, None, None, None, None, None, None, None, None, None))
    connect_database.commit()
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Комплексы \U0001F9EA", callback_data="group_buttons")
    keyboard.button(text="Поиск \U0001F50E", callback_data="search_analysis")
    keyboard.button(text="Стоп лист \u26D4\ufe0f", callback_data="stop_list")
    keyboard.adjust(1)
    await message.answer(text="\U000027A1 В режиме \U0001F50E Поиск введите название анализа по отдельности.. ",
                         reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "back_to_analyses")
async def process_back_to_analyses(call: CallbackQuery):
    await call.message.edit_text(text="\U000027A1 В режиме \U0001F50E Поиск введите название анализа по отдельности..",
                                 reply_markup=await base_menu_analyses())


# ==========================================================================================================
#                                       ПОИСК АНАЛИЗОВ:
# ==========================================================================================================
@router.callback_query(F.data == "search_analysis")
async def process_go_to_search_analysis(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_search)
    await call.message.edit_text(text="\U000026A0 ВНИМАНИЕ \U0000203C"
                                      "\n=================="
                                      "\n Как правильно выполнить <b>поиск</b>: "
                                      "\n1. Общий анализ крови"
                                      "\n2. ОАК  либо оак"
                                      "\n3. Корь, корь либо Measles Virus"
                                      "\n=================="
                                      '\n Нельзя: '
                                      "\n1. <s>сдать анализ на ОАК</s>"
                                      "\n2. <s>ОАК, ОАМ, ферритин, Витамин д</s>"
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
    stop_analysis = database_db.execute("""SELECT stop FROM analyses WHERE sequence_number = ?""",
                                        (idAnalyses,)).fetchone()[0]
    all_analyses = database_db.execute("""SELECT * FROM analyses WHERE sequence_number = ?""", (idAnalyses,))

    name_analysis = ""
    if stop_analysis == 1:
        for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price, prime_cost,
                stop, commplex) in enumerate(all_analyses.fetchall(), start=1):
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

    result = database_db.execute("""SELECT * FROM analyses WHERE sequence_number = ?""", (idAnalyses,)).fetchall()

    text_for_added = ""
    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price, prime_cost,
            stop, commplex) in enumerate(result, start=1):
        income = price - prime_cost
        database_db.execute(f"INSERT OR IGNORE INTO users_analyses_selected VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (sequence_number, analysis.split('(')[0], tube, readiness, price, prime_cost, income,
                             user_id))
        connect_database.commit()

        text_for_added = (f"{analysis.split('(')[0]}"
                          "\n==========================="
                          "\n\U00002705 Добавлено в КОРЗИНУ!")

    await call.message.edit_text(text=text_for_added, reply_markup=await kb_previous_search())


# ОБРАБОТКА КНОПКИ КАЖДОЙ ФУНКЦИИ АНАЛИЗА (ИНФО)
@router.callback_query(F.data.startswith('infoAn_'))
async def processing_found_analysis_info(call: CallbackQuery):
    idAnalyses = (call.data.split('infoAn_')[1]).split("-")[0]

    result = database_db.execute("""SELECT * FROM analyses WHERE sequence_number = ?""", (idAnalyses,)).fetchall()

    outcome = ""
    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price, prime_cost,
            stop, commplex) in enumerate(result, start=1):
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
    idAnalyses = (call.data.split('delAn_')[1]).split("-")[0]

    name_analysis = database_db.execute("""SELECT name FROM analyses WHERE sequence_number = ?""",
                                        (idAnalyses,)).fetchone()[0]

    database_db.execute(f"DELETE FROM users_analyses_selected WHERE code_analyses = ?", (idAnalyses,))
    connect_database.commit()

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
@router.callback_query(F.data.startswith("grp_"))
async def process_complex_watch(call: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    try:
        name = call.data.split('grp_')[1]
        text_output = all_complex(name)

        async def kb_info_complex():
            keyboard.button(text="добавить", callback_data=f"addSlctd_{name}")
            keyboard.button(text="удалить", callback_data=f"delSlctd_{name}")
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
    name_complex = call.data.split('addSlctd_')[1]
    # ======================================================================================================
    database_db.execute("""SELECT * FROM analyses WHERE complex = ?""", (name_complex,))
    result = database_db.fetchall()
    # ======================================================================================================
    outcome = ""

    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price, prime_cost,
            stop, commplex) in enumerate(result, start=1):
        income = price - prime_cost
        database_db.execute(f"INSERT OR IGNORE INTO users_analyses_selected VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (code_number, analysis, tube, readiness, price, prime_cost, income, user_id))
        connect_database.commit()
        outcome = "\U00002705 Добавлено в Корзину!"

    async def kb_buttons_in():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="group_buttons")
        keyboard.adjust(1)
        return keyboard.as_markup()

    await call.message.edit_text(text="Комплекс: " + name_complex + "\n" + outcome, reply_markup=await kb_buttons_in())


@router.callback_query(F.data.startswith("delSlctd_"))
async def process_komplex_add(call: CallbackQuery):
    user_id = call.message.chat.id

    database_db.execute(f"DELETE FROM users_analyses_selected WHERE user_id = ?", (user_id,))
    connect_database.commit()
    outcome = "Удален из Корзины!"

    async def kb_buttons_in():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="корзина \U0001F4E5", callback_data="back_to_basket_menu")
        keyboard.button(text="назад \U000023EA", callback_data="group_buttons")
        keyboard.adjust(1)
        return keyboard.as_markup()

    await call.message.edit_text(text=outcome, reply_markup=await kb_buttons_in())


# ОБРАБОТКА КНОПКИ СТОП-ЛИСТА
@router.callback_query(F.data == "stop_list")
async def process_stop_list(call: CallbackQuery):
    stop_analyses = []
    database_db.execute("""SELECT * FROM analyses WHERE stop = ?""", (0,))
    result = database_db.fetchall()
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
