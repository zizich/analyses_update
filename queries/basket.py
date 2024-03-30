from db.base import basket_db, conn_basket, add_db, date_person_db, job_db, cursor_db, date_add_db, midwifery_conn, \
    connect_person_date, pattern_db, all_analysis_db, connect_added, profit_db, connect_profit, connect_pattern, \
    profit_income_db, connect_profit_income, order_done_db, connect_order_done


def get_city_basket(user_id):
    return basket_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]


def get_comment_basket(user_id):
    return basket_db.execute("""SELECT comment FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]


def get_delivery_basket(user_id):
    return basket_db.execute("""SELECT delivery FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]


def get_added_analyses(user_id):
    return add_db.execute(f"SELECT * FROM user_{user_id}").fetchall()


def get_added_date(user_id):
    return date_person_db.execute(f"SELECT date_add FROM date WHERE user = ?", (user_id,)).fetchall()[0]


def get_info_job():
    return job_db.execute("SELECT * FROM services").fetchall()


def get_info_users_in_basket(user_id):
    return basket_db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()


def get_info_job_by_city(city):
    return job_db.execute("SELECT * FROM services WHERE city = ?", (city,)).fetchall()


def set_info_users_in_basket(fio, birth_date, phone, email, address, city, user_id):
    basket_db.execute("UPDATE users SET fio = ?, birth_date = ?, phone = ?, email = ?, address = ?, city = ? "
                      "WHERE user_id = ?", (fio, birth_date, phone, email, address, city, user_id))
    conn_basket.commit()


def update_delivery_in_basket(text, user_id):
    basket_db.execute("""UPDATE users SET delivery = ? WHERE user_id = ?""", (text, user_id))
    conn_basket.commit()


def get_date_added_nurse_by_city(city):
    return date_add_db.execute("""SELECT * FROM nurse WHERE city = ?""", (city,)).fetchall()


def update_id_nurse_in_basket(nurse_id, user_id):
    basket_db.execute("""UPDATE users SET id_midwifery = ? WHERE user_id = ?""", (nurse_id, user_id))
    conn_basket.commit()


def update_emoji_in_date_nurse(emojis, date, nurse_id):
    date_add_db.execute(f"""UPDATE nurse SET done = ? WHERE date = ?""", (emojis, f"{date}_{nurse_id}"))
    midwifery_conn.commit()


def init_new_date_in_basket(user_id, date):
    date_person_db.execute("INSERT OR IGNORE INTO date (user, date_add) VALUES (?, ?)", (user_id, date))
    connect_person_date.commit()


def update_emoji_after_delete_date_in_basket(emojis, date):
    date_add_db.execute("UPDATE nurse SET done = ? WHERE date = ?", (emojis, date))
    midwifery_conn.commit()


def delete_date_in_basket(user_id):
    date_person_db.execute("DELETE FROM date WHERE user = ?", (user_id,))
    connect_person_date.commit()


def get_numbers_pattern(user_id, pattern_found):
    return pattern_db.execute(f"""SELECT analysis_numbers FROM user_{user_id} 
    WHERE date = ?""", (pattern_found,)).fetchone()[0]


def delete_pattern(user_id, pattern_delete_name):
    pattern_db.execute(f"""DELETE FROM user_{user_id} WHERE date = ?""", (pattern_delete_name,))
    connect_pattern.commit()


def get_name_analyses_in_list_basket(user_id, key):
    return add_db.execute(f"SELECT name FROM user_{user_id} WHERE id = ?", (key,)).fetchone()[0]


def delete_analyses_in_list_basket(user_id, key):
    add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (key,))
    connect_added.commit()


def delete_all_analyses(user_id):
    add_db.execute(f"DELETE FROM user_{user_id}")
    connect_added.commit()


def delete_all_analyses_in_profit(user_id):
    profit_db.execute(f"DELETE FROM user_{user_id}")
    connect_profit.commit()


def update_new_comment_in_basket(comment, user_id):
    basket_db.execute("""UPDATE users SET comment = ? WHERE user_id = ?""",
                      (comment, user_id))
    conn_basket.commit()


def create_new_table_orders(user_id):
    basket_db.execute(f"""
        CREATE TABLE IF NOT EXISTS user_{user_id}(
            id_date TEXT PRIMARY KEY,
            name TEXT,
            analysis TEXT,
            price INTEGER,
            address TEXT,
            city TEXT,
            delivery TEXT,
            comment TEXT,
            id_midwifery TEXT,
            confirm TEXT
        )
        """)


def get_info_profit(user_id):
    return profit_db.execute(f"""SELECT * FROM user_{user_id}""").fetchall()


def init_new_profit_income(result_date, fio_by_dir, string_long_info, prices, price_all_other_analyses,
                           price_all_income):
    profit_income_db.execute("""INSERT OR IGNORE INTO users (date, name, analyses, price, 
                                price_other, price_income) VALUES(?, ?, ?, ?, ?, ?)""",
                             (result_date, fio_by_dir, string_long_info, prices,
                              price_all_other_analyses, price_all_income))
    connect_profit_income.commit()


def init_new_orders_in_basket(user_id, result_date, message_name, analysis_all, user_address, prices, city,
                              delivery, comment, id_midwiferys):
    basket_db.execute(f"INSERT INTO user_{user_id} (id_date, name, analysis, address, "
                      "price, city, delivery, comment, id_midwifery, confirm) "
                      "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (result_date, message_name, analysis_all, user_address, prices, city,
                       delivery, comment, id_midwiferys, "не подтверждена"))
    conn_basket.commit()


def init_new_order_nurse(id_midwiferys, result_date, message_name, analysis_by_order_done, tube, city, delivery,
                         user_address, comment, text_1, text_2, user_id, prices, price_all_other_analyses,
                         price_all_income):
    order_done_db.execute(f"INSERT INTO user_{id_midwiferys} (id_date, name, list_analysis, tube, "
                          "city, delivery, address, comment, done, confirm, user, price, cost_price, income) "
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (result_date, message_name, analysis_by_order_done, tube, city, delivery,
                           user_address, comment, text_1, text_2, user_id, prices,
                           price_all_other_analyses, price_all_income))
    connect_order_done.commit()


def delete_user_in_basket(user_id):
    basket_db.execute(f"DELETE FROM users WHERE user_id = ?", (user_id,))
    conn_basket.commit()
