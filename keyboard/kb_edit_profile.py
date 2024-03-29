from aiogram.utils.keyboard import InlineKeyboardBuilder


async def edit_user():
    kb_editProfile = InlineKeyboardBuilder()

    kb_editProfile.button(text="ФИО", callback_data="edit_fio_user"),
    kb_editProfile.button(text="дата рожд. \U0001F389", callback_data="edit_birth_date_user"),
    kb_editProfile.button(text="номер ☎️:", callback_data="edit_phone_user"),
    kb_editProfile.button(text="эл.почта \U0001F300", callback_data="edit_email_user"),
    kb_editProfile.button(text="город \U0001F3D8", callback_data="edit_city_user"),
    kb_editProfile.button(text="адрес \U0001F4EC", callback_data="edit_address_user")

    kb_editProfile.adjust(3)

    return kb_editProfile.as_markup()

