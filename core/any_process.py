import re
import datetime
from datetime import timedelta
from datetime import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import all_analysis_db

# TODO здесь будут хранится все файлы [] типа

# TODO №1 переменная list для обработки меню (ИНФО, ДОБАВИТЬ, УДАЛИТЬ) каждого, выбранного анализа
func_info_add_delete = ["add_analysis_in_basket", "delete_analysis_in_basket", "info_analysis_in_basket"]
peoples_collection = ["back_to_basket_menu", "first_child_add_basket", "second_child_add_basket",
                      "third_child_add_basket", "four_child_add_basket", "my_order_button", "others_order_button"]


# TODO ================================================================================================================

# TODO №2 функция для получения названия анализов на русском и возвращает на английском, для callback_data для кнопок
#  по КАТЕГОРИИ
def translate_any_each_analysis(name):
    for key, value in translate_each_analysis.items():
        if name == key:
            return value
        elif name == value:
            return key


# TODO =================================================================================================================
# TODO =================================================================================================================


# TODO №3 функция для получения названия анализов на русском и возвращает на английском, для callback_data для кнопок
#  по ПОИСКУ
def translate_any_number_analysis(name):
    for key, value in translate_number_analysis.items():
        if name == key:
            return value
        elif name == value:
            return key


# TODO функции для перевода букв и знаков ============================================================================
def translate(letter):
    rus_to_eng = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y',
        'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'X', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '1', 'Ы': 'YI', 'Ь': '2', 'Э': 'YE', 'Ю': 'YU',
        'Я': 'YA',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'x', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '1', 'ы': 'yi', 'ь': '2', 'э': 'ye', 'ю': 'yu',
        'я': 'ya', '!': "_", '@': "_", '#': "_", '$': "_", '%': "_", '^': "_", '&': "_", '*': "_", '(': "_", ')': "_",
        '-': "-",
        '+': "_", '=': "_", '{': "_", '}': "_", '[': "_", ']': "_", '|': "_", ':': ".", ';': "_", '<': "_", '>': "_",
        ',': "_", '.': ".", '?': "_", '/': "_", '_': "_", '~': "_", ' ': " ", "1": "1", "2": "2", "3": "3", "4": "4",
        "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "0": "0"
    }

    letter_collection = ""
    for in_key in letter:
        if in_key in rus_to_eng:
            letter_collection += rus_to_eng[in_key]
        else:
            letter_collection += in_key

    return letter_collection  # Если не найдено соответствие, возвращаем саму букву


def return_translate(name):
    string_done = []
    for letter in name:
        string_done.append(translate(letter))
    name_analysis = "".join(string_done)
    return name_analysis


# TODO =================================================================================================================


# TODO =================================================================================================================
#                                                  РАБОТА С БД СПИСКА АНАЛИЗОВ
# TODO =================================================================================================================

# TODO выводим с БД анализов

all_analysis_db.execute("SELECT * FROM clinic")

number_analysis = []  # TODO все порядковые номера анализов 411, 412, 413 и т.д.
translate_number_analysis = {}  # TODO словарь где ключ: анализ, значение: номер
rus_each_analysis = []  # TODO русское наименование анализов в виде коллекции
translate_each_analysis = {}  # TODO переменная для перевода каждого анализа на английский для кнопок
each_analysis_list = []  # TODO переменная для английского варианта анализа
any_word = {}

for i, (id_num, id_list, analysis, price, info, tube, readiness, sale, sale_number, price_other, stopped) in (
        enumerate(all_analysis_db.fetchall(), start=1)):
    number_analysis.append(str(id_num))
    translate_number_analysis["{}\nЦена: {}\u20BD".format(analysis.split('(')[0], price)] = str(id_num)
    rus_each_analysis.append(analysis)
    translate_each_analysis[analysis] = str(id_num)
    each_analysis_list.append(return_translate(analysis))


# TODO Функция для записи данных в файл
def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


def short_name(name_result):
    # Удаление пробелов по краям строки и цифр
    name_result = re.sub(r'\d+', '', name_result).strip()

    # Получение сокращенного имени
    name_parts = name_result.split()
    last_name = name_parts[0]
    first_initial = name_parts[1][0]
    second_initial = name_parts[2][0]

    abbreviated_name = f"{last_name} {first_initial}.{second_initial}."

    return abbreviated_name


# Функция для генерации 30 дней с сегодняшнего дня
def create_calendar(day):
    rus_day = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
    empty_day = ["\U0000274C", "\U0000274C", "\U0000274C", "\U0000274C", "\U0000274C", "\U0000274C", "\U0000274C"]
    slice_list = slice(day)
    new_list = empty_day[slice_list]
    today = datetime.now()
    inline_kb = InlineKeyboardBuilder()  # 7 days in a week
    for every_day in rus_day:
        inline_kb.button(text=f"{every_day}", callback_data=f"{every_day}")

    for element in range(31):
        new_list.append(f"{element}")

    count_empty = len(new_list) % 7
    count_filled = 7 - count_empty

    for num in range(count_filled):
        new_list.append("\U0000274C")

    for delta in new_list:
        if delta == "\U0000274C":
            inline_kb.button(text="\U0000274C", callback_data="\U0000274C")
        else:
            day = today + timedelta(days=int(delta))
            inline_kb.button(text=str(day.day), callback_data=f"day-{day.strftime('%d-%m-%Y')}")

    inline_kb.adjust(7)
    return inline_kb


# функция для генерации часов
def generate_time_keyboard(selected_date_str, *args):
    inline_kb = InlineKeyboardBuilder()  # 4 times in a row for better visibility
    selected_date = datetime.strptime(selected_date_str, "%d")
    start_time = datetime(selected_date.year, selected_date.month, selected_date.day, 6, 0)
    end_time = datetime(selected_date.year, selected_date.month, selected_date.day, 12, 30)
    while start_time < end_time:
        inline_kb.button(text=start_time.strftime("%H:%M"),
                         callback_data=f"time-{start_time.strftime('%H:%M')}")
        start_time += timedelta(minutes=30)
    inline_kb.adjust(5)
    return inline_kb
