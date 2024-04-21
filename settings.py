from dotenv import load_dotenv
import os


load_dotenv('.env')


class Config:
    # telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    SERVER_HOST = os.getenv('SERVER_HOST')
    SERVER_PORT = int(os.getenv('SERVER_PORT'))
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT'))
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
    DOMAIN = os.getenv('DOMAIN')
    WEBHOOK_URL = f'{DOMAIN}:{WEBHOOK_PORT}{WEBHOOK_PATH}'

    # postgres
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_NAME = os.getenv('DB_NAME')
    DB_PASS = os.getenv('DB_PASS')

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
