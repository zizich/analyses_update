import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from unittest import IsolatedAsyncioTestCase

from db.base import DB, Base
from test_utils.mixins import FactoryMixin


class InMemoryDBTestCase(IsolatedAsyncioTestCase):

    db = DB(url='sqlite+aiosqlite:///:memory:')
    session: AsyncSession = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db.setup()

    def setUp(self):
        super().setUp()
        self.session = self.db.session()

    async def asyncTearDown(self):
        await self.session.rollback()
        await self.session.close()


class AsyncTestCase(InMemoryDBTestCase, FactoryMixin):
    ...
