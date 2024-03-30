from unittest import IsolatedAsyncioTestCase

from sqlalchemy import select, text

from db.base import DB
from config import SQLITE_URL


class TestDBConnection(IsolatedAsyncioTestCase):
    TEST_DB_URL = SQLITE_URL

    async def test_connection(self):
        test_db = DB(url=self.TEST_DB_URL)
        test_db.setup()
        expected_result = to_select = 1

        async with test_db.session() as session:
            qs = await session.execute(select(to_select))
            existed_result = qs.scalars().first()

        self.assertEqual(existed_result, expected_result)

    async def test_db_query(self):
        test_db = DB(url=self.TEST_DB_URL)
        test_db.setup()

        async with test_db.session() as session:
            qs = await session.execute(text('SELECT * FROM nurse'))
            existed_result = qs.all()

        self.assertIsNotNone(existed_result)
