from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# соединяемся с БД списка общих анализов
from data_base import all_analysis_db, sur_analysis_db
from data_base import complex_analyses_db


# def all_clinic_analysis(group_name):
#     # инициализируем коллекцию
#     collection_without_duplicates = []
#
#     # выводим из БД список всех анализов и их параметров. Итерируем анализы по полученной группе (сортировка по
#     # уникальному номеру каждого анализа
#
#     all_analysis_db.execute("SELECT * FROM clinic")
#     result = all_analysis_db.fetchall()
#     for i, (sequence, id_list, name_analysis, price, info, tube, readiness, sale, sale_number, price_other, stop) in (
#             enumerate(result, start=1)):
#         name = translate_any_each_analysis(name_analysis)
#         if group_name == "clotheslining":
#             if 411 <= sequence <= 599:
#                 buttons_clotheslining = types.InlineKeyboardButton("{}-{}".format(price, name_analysis),
#                                                                  callback_data="{}".format(name))
#
#                 collection_without_duplicates.append(buttons_clotheslining)
#         elif group_name == "serology":
#             if 600 <= sequence <= 602:
#                 buttons_serology = types.InlineKeyboardButton("{}={}".format(name_analysis, price),
#                                                                  callback_data="{}".format(name))
#                 collection_without_duplicates.append(buttons_serology)
#
#     # полученный inline кнопки сортируем по уникальности, чтобы не было дубликатов
#     buttons = list(set(collection_without_duplicates))
#
#     # создаем inline кнопки по полученным значениям из списка БД
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     back = types.InlineKeyboardButton("назад", callback_data="group_buttons")
#     keyboard.add(*buttons).add(back)
#
#     return keyboard

def search_analyses(name_search, city):
    # инициализируем коллекцию
    keyboard = InlineKeyboardBuilder()

    # Выводим из БД список всех анализов и их параметров. Итерируем анализы по полученной группе (сортировка по
    # уникальному номеру каждого анализа, поиск осуществляется непосредственно по запросу SQL
    if city in "Сургут":
        dataBase = sur_analysis_db.execute(f"SELECT * FROM clinic WHERE "
                                           f"name_analysis LIKE '%{name_search}%' OR "
                                           f"name_analysis LIKE '%{name_search.capitalize()}%' OR "
                                           f"name_analysis LIKE '%{name_search.lower()}%' OR "
                                           f"name_analysis LIKE '%{name_search.upper()}%'")
    else:
        dataBase = all_analysis_db.execute(f"SELECT * FROM clinic WHERE "
                                           f"name_analysis LIKE '%{name_search}%' OR "
                                           f"name_analysis LIKE '%{name_search.capitalize()}%' OR "
                                           f"name_analysis LIKE '%{name_search.lower()}%' OR "
                                           f"name_analysis LIKE '%{name_search.upper()}%'")

    for i, (sequence, id_list, name_analysis, price, info, tube, readiness, sale, sale_number, price_other, stopped) \
            in enumerate(dataBase.fetchall(), start=1):
        keyboard.button(text="{}\u20BD: {}".format(price, name_analysis.split('(')[0]),
                        callback_data="id_{}-{}".format(sequence, city))
        # создаем inline кнопки по полученным значениям из списка БД
    return keyboard


# функция для сбора комплекса по запросу, возвращает строку
def all_complex(complex_in, city):
    selected = []  # для выбранных анализов
    sum_price = 0  # комплексная сумма передающая пользователю в консоль
    numbers_collection = []  # переменная для хранения порядкового номера анализа

    # ===========================================================================================================
    if city in "Сургут":
        result = sur_analysis_db.execute("SELECT * FROM clinic").fetchall()
    else:
        result = all_analysis_db.execute("SELECT * FROM clinic").fetchall()
    # ===========================================================================================================
    complex_analyses_db.execute("""SELECT * FROM complex""")
    complex_analysis = complex_analyses_db.fetchall()
    for y, (name_rus, name_eng, numbers) in enumerate(complex_analysis, start=1):
        if complex_in == name_eng:
            numbers_collection = [item.strip() for item in numbers.split(",")]
            break
    count_analysis = 1
    for i, (sequence, id_list, name_analysis, price, info, tube, readiness, sale, sale_number,
            price_other, *any_column) in enumerate(result, start=1):
        if sequence in map(int, numbers_collection):
            selected.append(f"\n{count_analysis}) {name_analysis} - {price} \U000020BD, срок: {readiness} дн.")
            sum_price += price
            count_analysis += 1

    text = "".join(selected)

    return text + f"\n==================\n<b>Общая сумма:</b> {sum_price} \U000020BD "


# функция реализующая получение выбранного комплекса, возврат всех входящих анализов
def all_complex_selected(complex_in):
    selected = []  # для выбранных анализов
    # ===========================================================================================================
    complex_analyses_db.execute("""SELECT * FROM complex""")
    complex_analysis = complex_analyses_db.fetchall()

    for y, (name_rus, name_eng, numbers) in enumerate(complex_analysis, start=1):
        if complex_in == name_eng:
            selected = [item.strip() for item in numbers.split(",")]
            break

    return selected
