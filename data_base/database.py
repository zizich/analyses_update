import sqlite3 as sq
import platform

system_info = platform.system()

# Подключение к базе данных ПЕРСОН
path_users = ""
if system_info == "Windows":
    path_users = "D:/Pro/database_server/database.db"
else:
    path_users = "/root/database_server/database.db"

connect_database = sq.connect(path_users)
database_db = connect_database.cursor()


