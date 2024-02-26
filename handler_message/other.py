from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import cursor_db

router = Router(name=__name__)


@router.message(F.text.in_('\U0001F465 Остальным'))
async def process_add_others_people(message: Message):
    user_id = message.from_user.id

    try:
        city = cursor_db.execute("""SELECT others_city FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

        cursor_db.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,))
        db_profile = cursor_db.fetchall()

        if db_profile[0][39] is not None:
            name_one = db_profile[0][39]
            female_one = db_profile[0][40]
            patronymic_one = db_profile[0][41]
            birth_date_one = db_profile[0][42]
            phone_one = db_profile[0][43]
            email_one = db_profile[0][44]
            address_one = db_profile[0][45]

            keyboard_one = InlineKeyboardBuilder()
            keyboard_one.button(text="редактировать", callback_data="edit_people_one")
            keyboard_one.button(text="удалить", callback_data="delete_people_one")
            keyboard_one.adjust(1)
            await message.answer("<b>Другим:</b>" + "\n" +
                                 f" 1️⃣  ♻️ ФИО: <b>{name_one}</b> <b>{female_one}</b> <b>{patronymic_one}</b>"
                                 + "\n" +
                                 f"     ♻️ Дата рождения: <b>{birth_date_one}</b>" + "\n" +
                                 f"     ♻️ Номер телефона: <b>{phone_one}</b>" + "\n" +
                                 f"     ♻️ e-mail: <b>{email_one}</b>" + "\n" +
                                 f"     ♻️ Город: <b>{city}</b> \U0001F3D8" + "\n" +
                                 f"     ♻️ Адресс: <b>{address_one}</b>",
                                 parse_mode=ParseMode.HTML, reply_markup=keyboard_one.as_markup())
        else:
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="добавить", callback_data="add_people_one")
            keyboard.adjust(1)
            await message.answer("Данных о наличии других людей - нет! ", reply_markup=keyboard.as_markup())
    except TypeError:
        await message.reply("Ошибка регистрации! Пройдите регистрацию!", reply_markup=ReplyKeyboardRemove())
