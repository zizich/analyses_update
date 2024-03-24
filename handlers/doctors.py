from aiogram import Router, F
from aiogram.types import Message

router = Router(name=__name__)


# =================================================================================================================
#                                                 ВРАЧИ
# =================================================================================================================
@router.message(F.text.in_('\U0001F468\U0000200D\U00002695\U0000FE0F Врачи'))
async def process_doctors(message: Message):
    # endocrin = types.InlineKeyboardButton("эндокринологи", callback_data="endocrinologist")
    # gastro = types.InlineKeyboardButton("гастроэнтерологи", callback_data="gastro")
    #
    # keyboard = types.InlineKeyboardMarkup(row_width=1)
    # keyboard.add(endocrin, gastro)

    await message.answer(text="\U0000267B\U0000FE0F Наши врачи всегда готовы Вам помочь!"
                              "\n\U0001F4CD эндокринолог"
                              "\n\U0001F4CD гастроэнтеролог"
                              "\nЗаписаться для ОНЛАЙН-консультации"
                              "\nможно по номеру <b>33-04-00</b>.")
