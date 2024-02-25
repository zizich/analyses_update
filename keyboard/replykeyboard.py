from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_menu():
    reply_keyboard_menu = ReplyKeyboardBuilder()
    reply_keyboard_menu.button(text='\U0001F3E0 Профиль')
    reply_keyboard_menu.button(text='\U0001F476 Дети')
    reply_keyboard_menu.button(text='\U0001F465 Остальным')
    reply_keyboard_menu.button(text='\U0001F489 Анализы')
    reply_keyboard_menu.button(text='\U0001F4D1 Заявки')
    reply_keyboard_menu.button(text="\U0001F6CD Акции")
    # result_analysis = KeyboardButton('\U0001F9FE Результаты')
    reply_keyboard_menu.button(text="\U0001F6D2 Корзина")
    reply_keyboard_menu.button(text="\U0001F468\U0000200D\U00002695\U0000FE0F Врачи")
    reply_keyboard_menu.button(text='\U0001F5C3 Архив заявок')
    reply_keyboard_menu.button(text='\U0001F4D7 Обратная связь')
    reply_keyboard_menu.adjust(3)

    return reply_keyboard_menu.as_markup(resize_keyboard=True)
