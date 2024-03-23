from aiogram.utils.keyboard import InlineKeyboardBuilder


async def kb_orders(result_the_end):
    # выводим все данные с БД basket пользователя на консоль

    keyboard = InlineKeyboardBuilder()

    for i, (date, users_id, nurse_id, name, analysis, price, address, city, delivery, comment,
            confirm) in enumerate(result_the_end, start=1):

        if confirm == "не подтверждена":
            emoji_str = "\U0000274C"
        else:
            emoji_str = "\u2705"
        keyboard.button(text=f"{date} {emoji_str}", callback_data=f"ordersShow_{date}")

    keyboard.adjust(2)

    return keyboard.as_markup()
