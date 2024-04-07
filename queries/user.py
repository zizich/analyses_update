from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.base import (cursor_db, connect_added, profit_db, connect_profit, basket_db, pattern_db, connect_pattern,
                     conn_basket, conn, job_db)


def get_user_by(user_id: int) -> tuple[str]:
    query = f"SELECT fio, birth_date, phone, email, city, address FROM users_{user_id} WHERE user_id = ?"
    cursor_db.execute(query, (f"{user_id}-1",))
    return cursor_db.fetchall()


def create_analyse(user_id) -> None:
    query = (f"CREATE TABLE IF NOT EXISTS user_{user_id} (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, "
             f"tube TEXT, readiness INTEGER)")
    connect_added.execute(query)
    connect_added.commit()


def create_user_profit_data(user_id: int):
    query = (f"CREATE TABLE IF NOT EXISTS user_{user_id} (id_list INTEGER, name_analysis TEXT, price TEXT, "
             f"price_other TEXT, price_income TEXT)")
    profit_db.execute(query)
    connect_profit.commit()


def create_user_order(user_id: int):
    basket_db.execute(f"""CREATE TABLE IF NOT EXISTS user_{user_id}(id_date TEXT, name TEXT, analysis TEXT, 
    price INTEGER, address TEXT, city TEXT, delivery TEXT, comment TEXT, id_midwifery TEXT, confirm TEXT)""")
    conn_basket.commit()  # new


def create_user_pattern(user_id: int):
    pattern_db.execute(
        f"CREATE TABLE IF NOT EXISTS user_{user_id}(date TEXT, name_pattern TEXT, analysis_numbers TEXT)")
    connect_pattern.commit()  # new


def create_user(user_id: int):
    cursor_db.execute(f"CREATE TABLE IF NOT EXISTS users_{user_id} (user_id TEXT PRIMARY KEY, fio TEXT, "
                      f"birth_date TEXT, phone INTEGER, email TEXT, city TEXT, address TEXT, subscribe TEXT, "
                      f"photo BLOB)")
    cursor_db.execute(f"INSERT OR IGNORE INTO users_{user_id} (user_id) VALUES (?)", (f"{user_id}-1",))
    conn.commit()


def choose_a_city():
    keyboard = InlineKeyboardBuilder()
    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityAdd_{city}")
    keyboard.adjust(1).as_markup()
    return keyboard


def edit_city_users():
    keyboard = InlineKeyboardBuilder()
    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cityEdit_{city}")
    keyboard.adjust(1).as_markup()
    return keyboard


def get_city_users(user_id) -> str:
    return cursor_db.execute(f"""SELECT city FROM users_{user_id} WHERE user_id = ?""", (user_id,)).fetchone()[0]


def set_city_basket(city, user_id):
    basket_db.execute("""UPDATE users SET city = ? WHERE user_id = ?""", (city, user_id))
    conn_basket.commit()


def set_city_users(city, user_id):
    cursor_db.execute(f"""UPDATE users_{user_id} SET city = ? WHERE user_id = ?""", (city, f"{user_id}-1"))
    conn.commit()


def set_info_users(user_id, fio, birth_date, phone, email, address):
    cursor_db.execute(
        f"""UPDATE users_{user_id} SET fio = ?, birth_date = ?, phone = ?, email = ?, address = ? 
                WHERE user_id = ?""", (fio, birth_date, phone, email, address, f"{user_id}-1"))
    conn.commit()


def edit_fio_users(user_id, message):
    cursor_db.execute(f"""UPDATE users_{user_id} SET fio = ? WHERE user_id = ?""",
                      (message, user_id))
    conn.commit()


def edit_birth_date_users(user_id, message):
    cursor_db.execute(f"""UPDATE users_{user_id} SET birth_date = ? WHERE user_id = ?""",
                      (message, user_id))
    conn.commit()


def edit_phone_users(user_id, message):
    cursor_db.execute(f"""UPDATE users_{user_id} SET phone = ? WHERE user_id = ?""",
                      (message, user_id))
    conn.commit()


def edit_email_users(user_id, message):
    cursor_db.execute(f"""UPDATE users_{user_id} SET email = ? WHERE user_id = ?""",
                      (message, user_id))
    conn.commit()


def edit_address_users(user_id, message):
    cursor_db.execute(f"""UPDATE users_{user_id} SET address = ? WHERE user_id = ?""",
                      (message, user_id))
    conn.commit()


def users_profile_info(user_id, id_user):
    cursor_db.execute(f"""SELECT user_id, fio, birth_date, phone, email, city, address FROM users_{user_id} 
    WHERE user_id = ?""", (id_user,))

    return cursor_db.fetchall()
