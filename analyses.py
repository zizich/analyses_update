import asyncio
import logging
import os
import re
import platform
import sqlite3 as sq
import aiogram
import locale
import datetime

from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm import storage

import registration
from data_base import (cursor_db, basket_db, date_add_db, all_analysis_db, add_db, order_done_db,
                       date_person_db, archive_db, profit_db, connect_profit, profit_income_db,
                       connect_profit_income, job_db, complex_analyses_db, midwifery_db, pattern_db,
                       connect_pattern, connect_sur_analysis, sur_analysis_db)
from data_base import (conn, conn_basket, midwifery_conn, conn_analysis, connect_added, connect_order_done,
                       connect_person_date, connect_archive, connect_job, conn_complex_analyses, connect_midwifery)

# from handler_message.start_command_handler import start_command

from config import BOT_TOKEN
from handler_message import start_command_handler
from handler_message.start_command_handler import States
from keyboard import reply_menu

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# Создание объекта хранилища

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

system_info = platform.system()


# ==============================================================================================================
#                                                   СТАРТ БОТА
# ==============================================================================================================
async def main():
    dp.include_router(start_command_handler.router)
    dp.include_router(registration.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")
