from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

reply_keyboard_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='\U0001F3E0 Мой профиль'), KeyboardButton(text='\U0001F465 Другие профили')],
    [KeyboardButton(text='\U0001F489 Анализы'), KeyboardButton(text="\U0001F6D2 Корзина"),
     KeyboardButton(text="\U0001F6CD Акции")],
    [KeyboardButton(text='\U0001F4D1 Заявки'),
     KeyboardButton(text="\U0001F468\U0000200D\U00002695\U0000FE0F Врачи"),
     KeyboardButton(text='\U0001F5C3 Архив заявок')],
    [KeyboardButton(text='\U0001F4D7 Обратная связь')]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню")
# reply_keyboard_menu.button(text='\U0001F3E0 Мой профиль')
# # reply_keyboard_menu.button(text='\U0001F476 Дети')
# reply_keyboard_menu.button(text='\U0001F465 Другие профили')
# reply_keyboard_menu.button(text='\U0001F489 Анализы')
# reply_keyboard_menu.button(text="\U0001F6D2 Корзина")
# reply_keyboard_menu.button(text="\U0001F6CD Акции")
# # result_analysis = KeyboardButton('\U0001F9FE Результаты')
# reply_keyboard_menu.button(text='\U0001F4D1 Заявки')
# reply_keyboard_menu.button(text="\U0001F468\U0000200D\U00002695\U0000FE0F Врачи")
# reply_keyboard_menu.button(text='\U0001F5C3 Архив заявок')
# reply_keyboard_menu.button(text='\U0001F4D7 Обратная связь')
# reply_keyboard_menu.adjust(3)
