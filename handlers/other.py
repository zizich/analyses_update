import uuid
import queries.others as query

from aiogram import Router, F
from aiogram.enums import ParseMode

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)


@router.message(F.text.in_('\U0001F465 Другие профили'))
async def process_add_others_people(message: Message):
    user_id = message.from_user.id

    db_profile = query.others_profile_info(user_id)

    keyboard = InlineKeyboardBuilder()
    try:
        unique_code = f"{uuid.uuid4()}"[:10]
        for i, (id_us, fio) in enumerate(db_profile, start=1):
            if id_us == f"{user_id}-1":
                pass
            else:
                keyboard.button(text=f"{fio}", callback_data=f"others_{id_us}")

        keyboard.button(text="добавить \U00002795", callback_data=f"people_{unique_code}")
        keyboard.adjust(1)
        await message.answer("Список: ", reply_markup=keyboard.as_markup())

    except TypeError:
        unique_code = f"{uuid.uuid4()}"[:10]
        keyboard.button(text="добавить \U00002795", callback_data=f"people_{unique_code}")
        keyboard.adjust(1)
        await message.answer("Список пуст!", reply_markup=keyboard.as_markup())


@router.callback_query(F.data == 'other_profile_back')
async def process_other_profile_back(call: CallbackQuery):
    user_id = call.message.chat.id

    db_profile = query.others_profile_info(user_id)

    keyboard = InlineKeyboardBuilder()
    try:
        async def kb_others_list():
            unique_code = f"{uuid.uuid4()}"[:10]
            for i, (id_us, fio) in enumerate(db_profile, start=1):

                if id_us == f"{user_id}-1":
                    pass
                else:

                    keyboard.button(text=f"{fio}", callback_data=f"others_{id_us}")

            keyboard.button(text="добавить \U00002795", callback_data=f"people_{unique_code}")
            keyboard.adjust(1)

            return keyboard.as_markup()

        await call.message.edit_text("Список: ", reply_markup=await kb_others_list())

    except TypeError:
        unique_cod = f"{uuid.uuid4()}"[:10]
        keyboard.button(text="добавить \U00002795", callback_data=f"people_{unique_cod}")
        keyboard.adjust(1)
        await call.message.answer("Список пуст!", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith("others_"))
async def process_show_other(call: CallbackQuery):
    user_id = call.message.chat.id
    unique_user = call.data.split("others_")[1]

    async def kb_other_user_info():
        keyboard_one = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="редактировать", callback_data=f"editPeople_{unique_user}"),
             InlineKeyboardButton(text="удалить", callback_data=f"delPeople_{unique_user}")],
            [InlineKeyboardButton(text="назад", callback_data="other_profile_back")]
        ])
        return keyboard_one

    db_profile = query.other_info(user_id, unique_user)

    try:
        for i, (id_us, fio, birth_date, phone, email, city, address, sub, photo) in enumerate(db_profile, start=1):
            await call.message.edit_text("<b>Другие профили:</b>" + "\n" +
                                         f"     ♻️ ФИО: <b>{fio}</b>"
                                         + "\n" +
                                         f"     ♻️ Дата рождения: <b>{birth_date}</b>" + "\n" +
                                         f"     ♻️ Номер телефона: <b>{phone}</b>" + "\n" +
                                         f"     ♻️ e-mail: <b>{email}</b>" + "\n" +
                                         f"     ♻️ Город: <b>{city}</b> \U0001F3D8" + "\n" +
                                         f"     ♻️ Адресс: <b>{address}</b>",
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=await kb_other_user_info())

            break
    except TypeError:
        await call.message.edit_text("Данных о наличии других людей - нет! ",
                                     reply_markup=await kb_other_user_info())
