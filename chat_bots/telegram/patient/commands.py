import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)


async def start(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await message.answer(
        f"Hi there! Your state: {current_state}",
        reply_markup=ReplyKeyboardRemove(),
    )


async def cancel(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def echo(message: Message, state: FSMContext) -> None:
    await message.send_copy(chat_id=message.chat.id)
