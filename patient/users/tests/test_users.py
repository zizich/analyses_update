from patient.users.dto import UserData
from patient.users.resources import UserResource
from utils.errors import ValidationError
from utils.tests.user_cases import DBAsyncTestCase


class TestUsers(DBAsyncTestCase):
    def setUp(self):
        super().setUp()
        self.resource = UserResource

    async def test_create_user_success(self):
        user_data = UserData(full_name='Иванов Иван Иванович', phone=80000123456, address='Сургут, Ленина, 1, 1')

        await self.resource.create(user_data=user_data)

        user_result = await self.resource.get()
        user = user_result.first()
        self.assertEqual(user_data.full_name, user.full_name)
        self.assertEqual(user_data.phone, user.phone)
        self.assertEqual(user_data.address, user.address)

    async def test_create_user_failed(self):
        user_data = UserData(full_name='Иванов Иван Иванович', phone=80000123456, address='Сургут, Ленина, 1, 1')
        await self.resource.create(user_data=user_data)

        with self.assertRaises(ValidationError) as ctx:
            await self.resource.create(user_data=user_data)

            self.assertEqual(ctx.exception.args[0], 'Пользователь с таким номером телефона уже существует.')

