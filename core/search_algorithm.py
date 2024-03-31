from aiogram.utils.keyboard import InlineKeyboardBuilder

# соединяемся с БД списка общих анализов
from data_base import database_db


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

def search_analyses(name_search):
    # инициализируем коллекцию
    keyboard = InlineKeyboardBuilder()

    # Выводим из БД список всех анализов и их параметров. Итерируем анализы по полученной группе (сортировка по
    # уникальному номеру каждого анализа, поиск осуществляется непосредственно по запросу SQL
    dataBase = database_db.execute(f"SELECT * FROM analyses WHERE "
                                   f"name LIKE '%{name_search}%' OR "
                                   f"name LIKE '%{name_search.capitalize()}%' OR "
                                   f"name LIKE '%{name_search.lower()}%' OR "
                                   f"name LIKE '%{name_search.upper()}%'")

    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price, prime_cost,
            stop, commplex) in enumerate(dataBase.fetchall(), start=1):
        keyboard.button(text="{}\u20BD: {}".format(price, analysis.split('(')[0]),
                        callback_data="id_{}".format(code_number))
        # создаем inline кнопки по полученным значениям из списка БД
    return keyboard


# функция для сбора комплекса по запросу, возвращает строку
def all_complex(code_complex):
    selected = []  # для выбранных анализов
    sum_price = 0  # комплексная сумма передающая пользователю в консоль

    # ===========================================================================================================
    # из кодировок анализов превращаем в коллекцию, для итерации в следующем цикле
    list_code_analyses = (database_db.execute("SELECT code_analyses FROM analyses_complex "
                                              "WHERE code_complex = ?", (code_complex,)).fetchone()[0]).split()
    # ===========================================================================================================
    result = database_db.execute("""SELECT * FROM analyses""")
    count = 0
    for i, (sequence_number, code_number, analysis, synonyms, info, tube, readiness, sale, price, prime_cost,
            stop, commplex) in enumerate(result, start=1):
        for code in list_code_analyses:
            if code_number in code:
                count += 1
                selected.append(f"\n{count}) {analysis} - {price} \U000020BD, срок: {readiness} дн.")
                sum_price += price

    text = "".join(selected)
    return text + f"\n==================\n<b>Общая сумма:</b> {sum_price} \U000020BD "

# функция реализующая получение выбранного комплекса, возврат всех входящих анализов
# def all_complex_selected(complex_in):
#     selected = []  # для выбранных анализов
#     # ===========================================================================================================
#     complex_analyses_db.execute("""SELECT * FROM complex""")
#     complex_analysis = complex_analyses_db.fetchall()
#
#     for y, (name_rus, name_eng, numbers) in enumerate(complex_analysis, start=1):
#         if complex_in == name_eng:
#             selected = [item.strip() for item in numbers.split(",")]
#             break
#
#     return selected
