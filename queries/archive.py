from db.base import (midwifery_db, archive_db, connect_archive)


def get_all_archive(user_id):
    return archive_db.execute(f"""SELECT * FROM user_{user_id}""").fetchall()


def get_info_nurse(nurse_id):
    return midwifery_db.execute("""SELECT * FROM users_midwifery WHERE user_id = ?""", (nurse_id,)).fetchall()


def clear_archive(user_id):
    archive_db.execute(f"""DROP TABLE IF EXISTS user_{user_id}""")
    connect_archive.commit()

