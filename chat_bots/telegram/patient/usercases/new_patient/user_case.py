from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from chat_bots.telegram import UserCase
from chat_bots.telegram.patient.usercases.new_patient.dto import ProfileDTO
from chat_bots.telegram.utils.actions import Approve, Edit


class NewPatient(UserCase):
    router: Router = Router()

    class States(StatesGroup):
        new_profile = State()
        approve_profile = State()
        edit_profile = State()

    @staticmethod
    async def entrypoint(message: Message, state: FSMContext):
        await state.set_state(NewPatient.States.new_profile)
        await message.answer(text=ProfileDTO.warning() + ProfileDTO.help())

    @staticmethod
    @router.message(States.new_profile)
    async def process_new_profile(message: Message, state: FSMContext) -> None:
        profile, err = ProfileDTO.parse_text(message.text)
        if err:
            await message.answer(text=err + ProfileDTO.warning())
            return

        await state.update_data(new_profile=profile)
        await state.set_state(NewPatient.States.approve_profile)
        await message.answer(
            f"Подтвердите, что указанные данные верны:\n{profile}",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=Approve.RU), KeyboardButton(text=Edit.RU)]], resize_keyboard=True,
            ),
        )

    @staticmethod
    @router.message(States.approve_profile, F.text == Edit.RU)
    async def process_dont_approve_profile(message: Message, state: FSMContext) -> None:
        await state.clear()
        await NewPatient.entrypoint(message, state)

    @staticmethod
    @router.message(States.approve_profile, F.text == Approve.RU)
    async def process_approve_profile(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(text='Ваш профиль успешно сохранен!', reply_markup=ReplyKeyboardRemove())

    @staticmethod
    @router.message()
    async def process_invalid_message(message: Message) -> None:
        await message.reply("I don't understand you :(")
