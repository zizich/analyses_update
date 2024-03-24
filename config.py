import os

# BOT_TOKEN = os.getenv('BOT_TOKEN', '')

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'analyses')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_HOST', '5432')


# todo
#  От решения ниже необходимо отказаться, в пользу хранения ТОКЕНА в переменных окружения
import platform
from data_base import job_db

system_info = platform.system()

BOT_TOKEN = ""
if system_info == "Windows":
    BOT_TOKEN = job_db.execute("""SELECT key FROM api_analyses WHERE system = ?""", (system_info,)).fetchone()[0]
elif system_info == "Linux":
    BOT_TOKEN = job_db.execute("""SELECT key FROM api_analyses WHERE system = ?""", (system_info,)).fetchone()[0]