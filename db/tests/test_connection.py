from unittest import IsolatedAsyncioTestCase

from sqlalchemy import select

from db.base import DBConnection


class TestDBConnection(IsolatedAsyncioTestCase):
    TEST_DB_URL = 'sqlite+aiosqlite:///:memory:'

    async def test_connection(self):
        test_db = DBConnection(url=self.TEST_DB_URL)
        expected_response, request_data = 1, 1

        async with test_db.async_session_ctx() as session:
            qs = await session.execute(select(request_data))
            existed_response = qs.scalars().first()

        self.assertEqual(expected_response, existed_response)
