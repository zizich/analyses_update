from db.base import (basket_db, conn_basket, job_db, date_add_db, midwifery_conn, pattern_db, all_analysis_db,
                     connect_pattern, profit_income_db, connect_profit_income, order_done_db, connect_order_done,
                     midwifery_db, archive_db, connect_archive)


def get_all_orders(user_id):
    return basket_db.execute(f"SELECT * FROM user_{user_id}").fetchall()


def get_info_payment(city) -> str:
    return job_db.execute("""SELECT bank, phone FROM services WHERE city = ?""", (city,)).fetchone()[0]


def get_address_point(city):
    return job_db.execute("""SELECT address FROM services WHERE city = ?""", (city,)).fetchone()[0]


def del_orders(user_id, del_date, date):
    # Удаляем подтвержденную заявку
    basket_db.execute(f"DELETE FROM user_{user_id} WHERE id_date = ?", (del_date,))
    conn_basket.commit()

    # восстанавливаем дату в БД у фельдшеров

    # добавляем в БД фельдшера выбранную дату со значком "галочка"
    date_add_db.execute(f"""UPDATE nurse SET done = ? WHERE date = ?""", ("\U0001F4CC", date))
    midwifery_conn.commit()

    # удаляем запись с БД (order_done) фельдшеров
    order_done_db.execute(f"DELETE FROM user_{date.split('_')[1]} WHERE id_date = ?", (del_date,))
    connect_order_done.commit()

    # удаляем запись с БД profit_income_db
    profit_income_db.execute("DELETE FROM users WHERE date = ?", (del_date,))
    connect_profit_income.commit()


def get_analyses_in_basket(user_id, transfer_date):
    return basket_db.execute(f"""SELECT analysis FROM user_{user_id} WHERE id_date = ?""", (transfer_date,)).fetchone()


def set_pattern(user_id, transfer_date, input_text, str_numbers_for_save_analysis):
    pattern_db.execute(f"""INSERT OR IGNORE INTO user_{user_id} (date, name_pattern, analysis_numbers) 
        VALUES (?, ?, ?)""", (transfer_date, input_text, str_numbers_for_save_analysis))
    connect_pattern.commit()


def init_new_archive(user_id):
    archive_db.execute(
        f"""CREATE TABLE IF NOT EXISTS user_{user_id} (
            id_date TEXT,
            name TEXT,
            analysis TEXT,
            price INTEGER,
            address TEXT,
            city TEXT,
            delivery TEXT,
            comment TEXT,
            confirm TEXT,
            id_midwifery TEXT
            )""")
    connect_archive.commit()


def set_info_in_archive(user_id, date, name, analysis, price, address, city, delivery, comm, confirm, id_midwifery):
    archive_db.execute(f"""INSERT OR IGNORE INTO user_{user_id} (id_date, name, analysis, price, address, city, 
                delivery, comment, confirm, id_midwifery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (date, name, analysis, price, address, city, delivery, comm, confirm, id_midwifery))
    connect_archive.commit()


def clear_basket(user_id, date):
    basket_db.execute(f"""DELETE FROM user_{user_id} WHERE id_date = ?""", (date,))
    conn_basket.commit()
