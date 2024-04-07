from db.base import archive_db, connect_archive


def get_info_archive(user_id):
    return archive_db.execute(f"""SELECT * FROM user_{user_id}""").fetchall()


def send_request(user_id, date):
    archive_db.execute(f"""UPDATE user_{user_id} SET confirm = ? WHERE id_date = ?""", ("нету результата", date))
    connect_archive.commit()

