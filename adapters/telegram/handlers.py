import contextlib
import logging
import sys
from typing import Any

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.getLogger('aiogram').setLevel(logging.DEBUG)


async def command_start_handler(message: Message) -> None:
    logging.debug(f"Received command_start: {message}")
    """This handler receives messages with `/start` command"""
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def command_custom(message: Message):
    logging.debug(f"Received command_start: {message}")
    """This handler receives messages with `/custom` command"""
    await message.answer(
        text=f"Видно ||Не видно||",
        # reply_markup=InlineKeyboardBuilder(markup=[[InlineKeyboardButton(text='button', callback_data='callback')]]).as_markup(),
        parse_mode='MarkdownV2'
    )


async def callback_handler(call: CallbackQuery):
    logging.debug(call.data)
    logging.debug(call.message)
    await call.answer(text="Done")


async def echo_handler(message: types.Message) -> Any | None:
    logging.debug(f"Received message: {message}")
    with contextlib.suppress(TypeError):
        return await message.send_copy(chat_id=message.chat.id)

    await message.answer("Nice try!")
