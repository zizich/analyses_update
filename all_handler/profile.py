from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import cursor_db

router = Router(name=__name__)


@router.message(F.text.in_(["\U0001F3E0 Профиль"]))
async def process_profile(message: Message):
    user_id = message.from_user.id

    try:
        city = cursor_db.execute("""SELECT city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

        cursor_db.execute("""SELECT user_id, name, female, patronymic, birth_date, phone, email, address
         FROM users WHERE user_id = ?""", (user_id,))
        db_profile = cursor_db.fetchall()
        id_user = db_profile[0][0]
        name = db_profile[0][1]
        female = db_profile[0][2]
        patronymic = db_profile[0][3]
        birth_date = db_profile[0][4]
        phone = db_profile[0][5]
        email = db_profile[0][6]
        home_address = db_profile[0][7]

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="\U0001F58D редактировать", callback_data="edit_profile")
        keyboard.adjust(1)
        await message.answer(text="<b>\U0001F3E0 Профиль:</b>" + "\n" +
                                  f"     ♻️ Ваш id:   <b>{id_user}</b>" + "\n" +
                                  f"     ♻️ Имя:   <b>{name}</b>" + "\n" +
                                  f"     ♻️ Фамилия: <b>{female}</b>" + "\n" +
                                  f"     ♻️ Отчество: <b>{patronymic}</b>" + "\n" +
                                  f"     ♻️ Дата рождения: <b>{birth_date}</b>" + "\n" +
                                  f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                  f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                  f"     ♻️ Город: <b>{city}</b> \U0001F3E0" + "\n" +
                                  f"     ♻️ Адресс: <b>{home_address}</b>",

                             parse_mode=ParseMode.HTML, reply_markup=keyboard.as_markup())
    except TypeError:
        await message.reply("Ошибка регистрации! Пройдите регистрацию!"
                            " Нажмите на меню -> start", reply_markup=ReplyKeyboardRemove())
