from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data_base import cursor_db

router = Router(name=__name__)


@router.message(F.text.in_('\U0001F465 Другие профили'))
async def process_add_others_people(message: Message):
    user_id = message.from_user.id

    cursor_db.execute(f"""SELECT user_id, fio FROM users_{user_id}""")
    db_profile = cursor_db.fetchall()

    keyboard = InlineKeyboardBuilder()
    try:
        count_other = 1
        for i, (user_id, fio) in enumerate(db_profile, start=1):
            count_other += 1
            keyboard.button(text=f"{fio}", callback_data=f"others_{user_id}-{count_other}")

        keyboard.button(text="добавить \U00002795", callback_data=f"people_{count_other}")
        keyboard.adjust(1)
        await message.answer("Список: ", reply_markup=keyboard.as_markup())

    except TypeError:
        await message.reply("Ошибка регистрации! Пройдите регистрацию!", reply_markup=ReplyKeyboardRemove())


@router.message(F.data == 'other_profile_back')
async def process_other_profile_back(message: Message):
    user_id = message.from_user.id

    cursor_db.execute(f"""SELECT user_id, fio FROM users_{user_id}""")
    db_profile = cursor_db.fetchall()

    keyboard = InlineKeyboardBuilder()
    try:
        count_other = 1
        for i, (id_user, fio) in enumerate(db_profile, start=1):
            count_other += 1
            keyboard.button(text=f"{fio}", callback_data=f"others_{id_user}")

        keyboard.button(text="добавить \U00002795", callback_data=f"people_{user_id}-{count_other + 1}")
        keyboard.adjust(1)
        await message.answer("Список: ", reply_markup=keyboard.as_markup())

    except TypeError:
        await message.reply("Ошибка регистрации! Пройдите регистрацию!", reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data.startswith("others_"))
async def process_show_other(call: CallbackQuery):
    user_id = call.message.chat.id
    user = call.data.split("others_")[1]

    cursor_db.execute(f"""SELECT * FROM users_{user_id} WHERE user_id = ?""", (user,))
    db_profile = cursor_db.fetchall()

    if db_profile[0][39] is not None:
        fio = db_profile[0][1]
        birth_date = db_profile[0][2]
        phone = db_profile[0][3]
        email = db_profile[0][4]
        city = db_profile[0][5]
        address = db_profile[0][6]

        keyboard_one = InlineKeyboardBuilder()
        keyboard_one.button(text="редактировать", callback_data="edit_people_one")
        keyboard_one.button(text="удалить", callback_data="delete_people_one")
        keyboard_one.adjust(1)
        await call.message.answer("<b>Другим:</b>" + "\n" +
                                  f" 1️⃣  ♻️ ФИО: <b>{fio}</b>"
                                  + "\n" +
                                  f"     ♻️ Дата рождения: <b>{birth_date}</b>" + "\n" +
                                  f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                  f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                  f"     ♻️ Город: <b>{city}</b> \U0001F3D8" + "\n" +
                                  f"     ♻️ Адресс: <b>{address}</b>",
                                  parse_mode=ParseMode.HTML, reply_markup=keyboard_one.as_markup())
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="редактировать", callback_data=f"editPeople_{user}")
        keyboard.button(text="удалить", callback_data=f"delPeople_{user}")
        keyboard.button(text="назад", callback_data="other_profile_back")
        keyboard.adjust(1)
        await call.message.answer("Данных о наличии других людей - нет! ", reply_markup=keyboard.as_markup())
