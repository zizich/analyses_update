import asyncio
import logging
import platform
import locale


from aiogram import Bot, Dispatcher


from config import BOT_TOKEN
from all_handler import start_command_handler, profile, childs, other, search_analyses, basket
from registration import first_registration, edit_user, edit_childs, edit_other

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
    dp.include_router(first_registration.router)
    dp.include_router(profile.router)
    dp.include_router(edit_user.router)
    dp.include_router(childs.router)
    dp.include_router(edit_childs.router)
    dp.include_router(other.router)
    dp.include_router(edit_other.router)
    dp.include_router(search_analyses.router)
    dp.include_router(basket.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")
