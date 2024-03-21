from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import database_db

router = Router(name=__name__)


@router.message(F.text.in_(["\U0001F3E0 Мой профиль"]))
async def process_profile(message: Message):
    user_id = message.from_user.id

    database_db.execute("""SELECT fio, birth_date, phone, email, city, address FROM users WHERE user_id = ?""",
                        (user_id,))
    try:
        for i, (fio, birth_date, phone, email, city, address) in enumerate(database_db.fetchall(), start=1):
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="\U0001F58D редактировать", callback_data="edit_profile")
            keyboard.adjust(1)
            await message.answer(text=f"<b>\U0001F3E0 Профиль:</b>"
                                      f"\n    ♻️ Ваш id:   <b>{user_id}</b>"
                                      f"\n    ♻️ ФИО:   <b>{fio}</b>"
                                      f"\n    ♻️ Номер телефона: <b>{phone}</b>"
                                      f"\n    ♻️ e-mail: <b>{email}</b>"
                                      f"\n    ♻️ Город: <b>{city}</b> \U0001F3E0"
                                      f"\n    ♻️ Адресс: <b>{address}</b>",
                                 reply_markup=keyboard.as_markup())
    except TypeError:
        await message.reply("Ошибка регистрации! Пройдите регистрацию!"
                            " Нажмите на меню -> start", reply_markup=ReplyKeyboardRemove())
