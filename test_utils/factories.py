from datetime import date

from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models.users import User


DEFAULT_USER_DATA = {
    'fio': 'Иванов Иван Иванович',
    'birth_date': date(year=1970, month=1, day=1),
    'phone': '+71234123456',
    'city': 'Сургут',
}


def create_user(session, **kwargs) -> User:
    DEFAULT_USER_DATA.update(kwargs)
    user = User(**DEFAULT_USER_DATA)
    session.add(user)
    return user


def create_inline_keyboard(keyboard_data: tuple[tuple[str, str], ...]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for text, callback_data in keyboard_data:
        keyboard.button(text=text, callback_data=callback_data)
    return keyboard
