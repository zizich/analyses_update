import functools
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, ANY

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from chat_bots.telegram.patient.usercases import NewPatient
from chat_bots.telegram.patient.usercases.new_patient.dto import ProfileDTO


class TestNewPatient(IsolatedAsyncioTestCase):

    def setUp(self):
        self.user_case = NewPatient()
        self.message = AsyncMock(answer=AsyncMock())
        self.fsm_builder = functools.partial(FSMContext, storage=MemoryStorage(), key='test')

    async def test_entrypoint(self):
        fsm_context: FSMContext = self.fsm_builder()
        await self.user_case.entrypoint(message=self.message, state=fsm_context)

        self.message.answer.assert_called_once_with(text=ProfileDTO.warning() + ProfileDTO.help())
        new_state = await fsm_context.get_state()
        self.assertTrue(new_state == self.user_case.States.new_profile)

    async def test_process_new_profile_success(self):
        text_from_user = 'Иванов Иван Иванович\n80000123456\nСургут, Ленина, 1, 1'
        self.message.text = text_from_user
        fsm_context: FSMContext = self.fsm_builder()
        await fsm_context.set_state(self.user_case.States.new_profile)

        await self.user_case.process_new_profile(message=self.message, state=fsm_context)

        profile, _ = ProfileDTO.parse_text(text_from_user)
        self.message.answer.assert_called_once_with(f'Подтвердите, что указанные данные верны:\n{profile}', reply_markup=ANY)
        self.assertEqual(await fsm_context.get_state(), self.user_case.States.approve_profile)
        self.assertEqual(await fsm_context.get_data(), dict(new_profile=profile))

    async def test_process_new_profile_failed(self):
        text_from_user = 'Иванов Иван Иванович, 80000123456, Сургут, Ленина, 1, 1'
        self.message.text = text_from_user
        fsm_context: FSMContext = self.fsm_builder()
        await fsm_context.set_state(self.user_case.States.new_profile)

        await self.user_case.process_new_profile(message=self.message, state=fsm_context)

        _, err_msg = ProfileDTO.parse_text(text_from_user)
        self.message.answer.assert_called_once_with(text=err_msg + ProfileDTO.warning())
        self.assertEqual(await fsm_context.get_state(), self.user_case.States.new_profile)
        self.assertEqual(await fsm_context.get_data(), {})

    async def test_process_dont_approve_profile(self):
        fsm_context: FSMContext = self.fsm_builder()
        await fsm_context.set_state(self.user_case.States.approve_profile)
        saved_data = dict(my_data='Test')
        await fsm_context.update_data(**saved_data)

        await self.user_case.process_dont_approve_profile(message=self.message, state=fsm_context)

        self.message.answer.assert_called_once_with(text=ProfileDTO.warning() + ProfileDTO.help())
        self.assertEqual(await fsm_context.get_state(), self.user_case.States.new_profile)
        self.assertEqual(await fsm_context.get_data(), {})

    async def test_process_approve_profile(self):
        fsm_context: FSMContext = self.fsm_builder()
        await fsm_context.set_state(self.user_case.States.approve_profile)
        saved_data = dict(my_data='Test')
        await fsm_context.update_data(**saved_data)

        await self.user_case.process_dont_approve_profile(message=self.message, state=fsm_context)

        self.message.answer.assert_called_once_with(text='Ваш профиль успешно сохранен!')
        self.assertEqual(await fsm_context.get_state(), None)
        self.assertEqual(await fsm_context.get_data(), saved_data)
