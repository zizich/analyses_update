import sqlite3 as sq
import os
import platform

system_info = platform.system()

# Подключение к базе данных ПЕРСОН
path_users = ""
if system_info == "Windows":
    path_users = "D:/Pro/database_server/database.db"
else:
    path_users = "/root/database_server/database.db"

conn = sq.connect(path_users)
cursor_db = conn.cursor()

cursor_db.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    female TEXT,
    patronymic TEXT,
    birth_date TEXT,
    phone INTEGER,
    email TEXT,
    address TEXT,
    city TEXT,
    subscribe_date_doctor TEXT, 
    photo_analysis BLOB,
    child_name TEXT,
    child_female TEXT,
    child_patronymic TEXT,
    child_birth_date TEXT,
    child_subscribe_date_analysis TEXT,
    child_subscribe_date_doctor TEXT, 
    child_photo_analysis BLOB,
    two_child_name TEXT,
    two_child_female TEXT,
    two_child_patronymic TEXT,
    two_child_birth_date TEXT,
    two_child_subscribe_date_analysis TEXT,
    two_child_subscribe_date_doctor TEXT, 
    two_child_photo_analysis BLOB,
    three_child_name TEXT,
    three_child_female TEXT,
    three_child_patronymic TEXT,
    three_child_birth_date TEXT,
    three_child_subscribe_date_analysis TEXT,
    three_child_subscribe_date_doctor TEXT, 
    three_child_photo_analysis BLOB,
    four_child_name TEXT,
    four_child_female TEXT,
    four_child_patronymic TEXT,
    four_child_birth_date TEXT,
    four_child_subscribe_date_analysis TEXT,
    four_child_subscribe_date_doctor TEXT, 
    four_child_photo_analysis BLOB,
    others_name_one TEXT,
    others_female_one TEXT,
    others_patronymic_one TEXT,
    others_birth_date_one TEXT,
    others_phone_one INTEGER,
    others_email_one TEXT,
    others_address_one TEXT,
    others_city TEXT,
    others_subscribe_date_doctor_one TEXT, 
    others_photo_analysis_one BLOB

)""")

# КОНТАКТИРОВАТЬ С БАЗОЙ ДАННЫХ КОРЗИНЫ
path_basket = ""
if system_info == "Windows":
    path_basket = "D:/Pro/database_server/basket.db"
else:
    path_basket = "/root/database_server/basket.db"

conn_basket = sq.connect(path_basket)
basket_db = conn_basket.cursor()

basket_db.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    female TEXT,
    patronymic TEXT,
    birth_date TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    city TEXT,
    delivery TEXT,
    comment TEXT,
    id_midwifery TEXT
)
""")

#  TODO КОНТАКТИРОВАТЬ С БД ДАТЫ ВЫБОРА ФЕЛЬДШЕРОВ
path_to_db = ""
if system_info == "Windows":
    path_to_db = os.path.join("D:/Pro/database_server/date_add.db")
elif system_info == "Linux":
    path_to_db = os.path.join("/root/database_server/date_add.db")
midwifery_conn = sq.connect(path_to_db)
date_add_db = midwifery_conn.cursor()

# TODO соединяемся с БД списка анализов
path_all_analyses = ""
if system_info == "Windows":
    path_all_analyses = "D:/Pro/database_server/all_analysis.db"
else:
    path_all_analyses = "/root/database_server/all_analysis.db"

conn_analysis = sq.connect(path_all_analyses)
all_analysis_db = conn_analysis.cursor()

# TODO соединяемся с БД выбранных из списка анализов
path_added_analysis = ""
if system_info == "Windows":
    path_added_analysis = "D:/Pro/database_server/added_analysis.db"
else:
    path_added_analysis = "/root/database_server/added_analysis.db"

connect_added = sq.connect(path_added_analysis)
add_db = connect_added.cursor()

# TODO соединяемся с БД готовых заявок ДЛЯ ФЕЛЬДШЕРА
order = ""
if system_info == "Windows":
    order = os.path.join("D:/Pro/database_server/order_done.db")
elif system_info == "Linux":
    order = os.path.join("/root/database_server/order_done.db")
connect_order_done = sq.connect(order)
order_done_db = connect_order_done.cursor()

# TODO соединяемся с БД готовых заявок ДЛЯ ФЕЛЬДШЕРА
order_midwifery = ""
if system_info == "Windows":
    order_midwifery = os.path.join("D:/Pro/database_server/midwifery.db")
elif system_info == "Linux":
    order_midwifery = os.path.join("/root/database_server/midwifery.db")
connect_midwifery = sq.connect(order_midwifery)
midwifery_db = connect_midwifery.cursor()

# TODO соединяемся с БД выбранных из списка дат
path_added_date = ""
if system_info == "Windows":
    path_added_date = "D:/Pro/database_server/date_person.db"
else:
    path_added_date = "/root/database_server/date_person.db"

connect_person_date = sq.connect(path_added_date)
date_person_db = connect_person_date.cursor()

# TODO соединяемся с БД архив заявок
path_archive = ""
if system_info == "Windows":
    path_archive = "D:/Pro/database_server/archive.db"
else:
    path_archive = "/root/database_server/archive.db"

connect_archive = sq.connect(path_archive)
archive_db = connect_archive.cursor()

# TODO соединяемся с БД дохода
path_profit = ""
if system_info == "Windows":
    path_profit = os.path.join("D:/Pro/database_server/profit.db")
elif system_info == "Linux":
    path_profit = os.path.join("/root/database_server/profit.db")
connect_profit = sq.connect(path_profit)
profit_db = connect_profit.cursor()

# TODO соединяемся с БД дохода
path_income = ""
if system_info == "Windows":
    path_income = os.path.join("D:/Pro/database_server/profit_income.db")
elif system_info == "Linux":
    path_income = os.path.join("/root/database_server/profit_income.db")
connect_profit_income = sq.connect(path_income)
profit_income_db = connect_profit_income.cursor()

# TODO соединяемся с БД услугами (забор крови, выезд на дом)
path_job = ""
if system_info == "Windows":
    path_job = "D:/Pro/database_server/services_job.db"
else:
    path_job = "/root/database_server/services_job.db"

connect_job = sq.connect(path_job)
job_db = connect_job.cursor()

# TODO соединяемся с БД комплекс анализов
path_complex = ""
if system_info == "Windows":
    path_complex = "D:/Pro/database_server/complex_analyses.db"
else:
    path_complex = "/root/database_server/complex_analyses.db"

conn_complex_analyses = sq.connect(path_complex)
complex_analyses_db = conn_complex_analyses.cursor()

# TODO соединяемся с БД шаблонов
path_pattern = ""
if system_info == "Windows":
    path_pattern = "D:/Pro/database_server/pattern.db"
else:
    path_pattern = "/root/database_server/pattern.db"

connect_pattern = sq.connect(path_pattern)
pattern_db = connect_pattern.cursor()

# TODO соединяемся с БД шаблонов
path_sur = ""
if system_info == "Windows":
    path_sur = "D:/Pro/database_server/sur_analysis.db"
else:
    path_sur = "/root/database_server/sur_analysis.db"

connect_sur_analysis = sq.connect(path_sur)
sur_analysis_db = connect_sur_analysis.cursor()

