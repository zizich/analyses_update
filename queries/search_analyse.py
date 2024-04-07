from db.base import basket_db, conn_basket, all_analysis_db, add_db, connect_added, \
    profit_db, connect_profit, complex_analyses_db


def init_new_user_in_basket(user_id):
    basket_db.execute("""INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (user_id, None, None, None, None, None, None, None, None, None))
    conn_basket.commit()


def search_analys(name_search):
    return all_analysis_db.execute(f"SELECT * FROM clinic WHERE "
                                   f"name_analysis LIKE '%{name_search}%' OR "
                                   f"name_analysis LIKE '%{name_search.capitalize()}%' OR "
                                   f"name_analysis LIKE '%{name_search.lower()}%' OR "
                                   f"name_analysis LIKE '%{name_search.upper()}%'")


def all_analyses() -> tuple:
    return all_analysis_db.execute("SELECT * FROM clinic").fetchall()


def complex_analyses() -> tuple:
    return complex_analyses_db.execute("""SELECT * FROM complex""").fetchall()


def stop_analyses(id_analyses):
    return all_analysis_db.execute("""SELECT stopped FROM clinic WHERE id_list = ?""",
                                   (id_analyses,)).fetchone()[0]


def found_analyses(id_analyses):
    return all_analysis_db.execute("""SELECT * FROM clinic WHERE id_list = ?""", (id_analyses,)).fetchall()


def add_analyses(user_id, id_analysis, name_analysis, price, tube, readiness, price_other, price_income):
    add_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                   (id_analysis, name_analysis, price, tube, readiness))
    connect_added.commit()

    profit_db.execute(f"INSERT OR IGNORE INTO user_{user_id} VALUES (?, ?, ?, ?, ?)",
                      (id_analysis, name_analysis.split('(')[0], price, price_other, price_income))
    connect_profit.commit()


def delete_analyses_in_db(user_id, id_analyses):
    add_db.execute(f"DELETE FROM user_{user_id} WHERE id = ?", (id_analyses,))
    connect_added.commit()

    profit_db.execute(f"DELETE FROM user_{user_id} WHERE id_list = ?", (id_analyses,))
    connect_profit.commit()


def all_stop_analyses():
    return all_analysis_db.execute("""SELECT * FROM clinic WHERE stopped = ?""", (0,)).fetchall()
