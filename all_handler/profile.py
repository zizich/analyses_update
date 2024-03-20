from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import database_db

router = Router(name=__name__)


@router.message(F.text.in_(["\U0001F3E0 Мой профиль"]))
async def process_profile(message: Message):
    user_id = message.from_user.id

    try:
        database_db.execute(f"""SELECT user_id, fio, birth_date, phone, email, city, address, subscribe, info, others, 
        photo, reference FROM users WHERE user_id = ?""", (user_id,))
        db_profile = database_db.fetchall()
        id_user = db_profile[0][0]
        fio = db_profile[0][1]
        birth_date = db_profile[0][2]
        phone = db_profile[0][3]
        email = db_profile[0][4]
        city = db_profile[0][5]
        home_address = db_profile[0][6]

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="\U0001F58D редактировать", callback_data="edit_profile")
        keyboard.adjust(1)
        await message.answer(text="<b>\U0001F3E0 Профиль:</b>" + "\n" +
                                  f"     ♻️ Ваш id:   <b>{id_user}</b>" + "\n" +
                                  f"     ♻️ ФИО:   <b>{fio}</b>" + "\n" +
                                  f"     ♻️ Дата рождения: <b>{birth_date}</b>" + "\n" +
                                  f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                  f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                  f"     ♻️ Город: <b>{city}</b> \U0001F3E0" + "\n" +
                                  f"     ♻️ Адресс: <b>{home_address}</b>",

                             parse_mode=ParseMode.HTML, reply_markup=keyboard.as_markup())
    except TypeError:
        await message.reply("Ошибка регистрации! Пройдите регистрацию!"
                            " Нажмите на меню -> start", reply_markup=ReplyKeyboardRemove())
