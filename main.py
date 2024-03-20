import asyncio
import logging
import os
import locale
import platform
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

from all_handler import start_command_handler, profile, other, search_analyses, basket, orders, archive, sale, \
    feedback, doctors
from registration import first_registration, edit_user, edit_other

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# Создание объекта хранилища

load_dotenv(find_dotenv())

system_info = platform.system()

if system_info == "Windows":
    bot = Bot(token=os.getenv("BOT_TOKEN_W"), parse_mode="HTML")
else:
    bot = Bot(token=os.getenv("BOT_TOKEN_L"), parse_mode="HTML")

dp = Dispatcher()

system_info = platform.system()


# ==============================================================================================================
#                                                   СТАРТ БОТА
# ==============================================================================================================
async def main():
    dp.include_router(start_command_handler.router)
    dp.include_router(first_registration.router)
    dp.include_router(profile.router)
    dp.include_router(edit_user.router)
    dp.include_router(other.router)
    dp.include_router(edit_other.router)
    dp.include_router(search_analyses.router)
    dp.include_router(basket.router)
    dp.include_router(orders.router)
    dp.include_router(archive.router)
    dp.include_router(sale.router)
    dp.include_router(feedback.router)
    dp.include_router(doctors.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")
