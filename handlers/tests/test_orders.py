from unittest.mock import patch, call

from aiogram.types import Message

from handlers.orders import process_show_orders
from test_utils.mocks import Message, Chat
from test_utils.testcases import AsyncTestCase


class TestOrders(AsyncTestCase):

    async def asyncSetUp(self):
        user = self.create_user(id=1)
        chat = Chat(id=user.id)
        self.message = Message(id=user.id, chat=chat)
        self.order = [
            ('2024-04-01', 'name', 'analysis', 'price', 'address', 'city', 'delivery', 'comm', 'id_mid', 'подтеврждена'),
            ('2024-04-02', 'name', 'analysis', 'price', 'address', 'city', 'delivery', 'comm', 'id_mid', 'не подтверждена'),
        ]

    @patch('queries.orders.get_all_orders')
    async def test_process_show_orders(self, get_all_orders):
        get_all_orders.return_value = self.order

        await process_show_orders(message=self.message)

        self.message.answer.assert_awaited_once()
        confirm_button = ('2024-04-01   ✅', 'ordersShow_2024-04-01')
        not_confirm_button = ('2024-04-02   ❌', 'ordersShow_2024-04-02')
        _call = call(
            text='👉 Выберите заявку: ',
            reply_markup=self.create_inline_keyboard(keyboard_data=(confirm_button, not_confirm_button)).as_markup()
        )
        self.message.answer.assert_has_awaits([_call])
