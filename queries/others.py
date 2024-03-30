from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.base import (cursor_db, connect_added, profit_db, connect_profit, basket_db, pattern_db, connect_pattern,
                     conn_basket, conn, job_db)


def others_profile_info(user_id):
    return cursor_db.execute(f"""SELECT user_id, fio FROM users_{user_id}""").fetchall()


def other_info(user_id, unique_user):
    return cursor_db.execute(f"""SELECT * FROM users_{user_id} WHERE user_id = ?""", (unique_user,)).fetchall()


def choice_others_city():
    keyboard = InlineKeyboardBuilder()

    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"addCity_{city}")

    keyboard.adjust(1).as_markup()

    return keyboard


def set_all_info_others(user_id, unique_user, fio, birth_date, phone, email, city, address):
    cursor_db.execute(
        f"""INSERT OR IGNORE INTO users_{user_id} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (f"{unique_user}", fio, birth_date, phone, email, city, address, None, None))
    conn.commit()


def get_fio_others(user_id, unique_num):
    return cursor_db.execute(f"""SELECT fio FROM users_{user_id} WHERE user_id = ?""", (unique_num,)).fetchone()[0]


def del_others(user_id, unique_num):
    cursor_db.execute(f"""DELETE FROM users_{user_id} WHERE user_id = ? """, (f"{unique_num}",))
    conn.commit()


def get_others_profile(user_id, unique_num):
    return cursor_db.execute(f"""SELECT * FROM users_{user_id} WHERE user_id = ?""", (unique_num,)).fetchall()


def edit_fio_others(user_id, message, id_user):
    cursor_db.execute(f"""UPDATE users_{user_id} SET fio = ? WHERE user_id = ?""",
                      (message, id_user))
    conn.commit()


def edit_birth_date_others(user_id, message, send_unique_id):
    cursor_db.execute(f"""UPDATE users_{user_id} SET birth_date = ? WHERE user_id = ?""",
                      (message, send_unique_id))
    conn.commit()


def edit_phone_others(user_id, message, send_unique_id):
    cursor_db.execute(f"""UPDATE users_{user_id} SET phone = ? WHERE user_id = ?""",
                      (message, send_unique_id))
    conn.commit()


def edit_email_others(user_id, message, send_unique_id):
    cursor_db.execute(f"""UPDATE users_{user_id} SET email = ? WHERE user_id = ?""",
                      (message, send_unique_id))
    conn.commit()


def kb_edit_city_others(id_user):
    keyboard = InlineKeyboardBuilder()
    job_db.execute("""SELECT * FROM services""")
    for i, (city, sampling, out_pay, address, phone, bank, all_sale) in enumerate(job_db.fetchall(), start=1):
        keyboard.button(text=f"{city} \u23E9", callback_data=f"cPeople_{city}={id_user}")

    keyboard.adjust(1).as_markup()

    return keyboard


def edit_city_others(user_id, city, id_user):
    cursor_db.execute(f"""UPDATE users_{user_id} SET city = ? WHERE user_id = ?""",
                      (city, id_user))
    conn.commit()


def edit_address_others(user_id, message, send_unique_id):
    cursor_db.execute(f"""UPDATE users_{user_id} SET address = ? WHERE user_id = ?""",
                      (message, send_unique_id))
    conn.commit()


