from db.base import (basket_db, conn_basket, job_db, date_add_db, midwifery_conn, pattern_db, all_analysis_db,
                     connect_pattern, profit_income_db, connect_profit_income, order_done_db, connect_order_done,
                     midwifery_db, archive_db, connect_archive)


def get_id_nurse(user_id, date):
    return basket_db.execute(f"""SELECT id_midwifery FROM user_{user_id} WHERE id_date = ?""", (date,)).fetchone()[0]


def get_info_nurse(id_midwifery):
    return midwifery_db.execute("""SELECT * FROM users_midwifery WHERE user_id = ?""", (id_midwifery,)).fetchall()

