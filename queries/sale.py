from db.base import job_db, all_analysis_db, add_db, connect_added


def get_sale_in_city(city) -> str:
    return job_db.execute("""SELECT all_sale FROM services WHERE city = ?""", (city,)).fetchone()[0]


def get_sale_analyses():
    return all_analysis_db.execute("""SELECT * FROM clinic WHERE sale = ?""", ("yes",)).fetchall()


def add_sale_analyses(user_id, id_analysis, name_analysis, price_all, tube, readiness):
    add_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                   (id_analysis, name_analysis, price_all, tube, readiness))
    connect_added.commit()


def del_sale_analyses(user_id, id_analyses):
    add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (id_analyses,))
    connect_added.commit()

