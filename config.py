import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'password')
DB_NAME = os.getenv('DB_NAME', 'analyses')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_HOST', '5432')

POSTGRES_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

DB_FILE_PATH = os.getenv('DB_FILE_PATH', '')
SQLITE_URL = f'sqlite+aiosqlite:///{DB_FILE_PATH}'
