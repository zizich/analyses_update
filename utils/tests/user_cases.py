import asyncio
import tempfile
from typing import IO
from unittest import IsolatedAsyncioTestCase

from sqlalchemy import delete

from db.base import DBConnection, Base


class DBAsyncTestCase(IsolatedAsyncioTestCase):
    db: DBConnection
    temp_db: IO

    @classmethod
    def setUpClass(cls):
        # SqlAlchemy поддерживает "In Memmory" БД только в синхронном режиме.
        # Чтобы обойти это ограничение используем файловую БД
        cls.temp_db = tempfile.NamedTemporaryFile()
        cls.db = DBConnection(url=f'sqlite+aiosqlite:///{cls.temp_db.name}')

        # Создание таблиц игнорирует метод asyncSetUp, т.к.
        # Если запускать асинхронные тесты пачкой, может попасться кейс,
        # когда Тест запустится до того, как создастя Таблица в БД
        asyncio.run(cls.create_tables())

    @classmethod
    async def create_tables(cls):
        async with cls.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def asyncTearDown(self):
        await self.truncate_all_tables()

    async def truncate_all_tables(self):
        async with self.db.session() as session:
            for table in Base.metadata.sorted_tables:
                await session.execute(delete(table))
                await session.commit()

    @classmethod
    async def drop_tables(cls):
        async with cls.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await cls.db.engine.dispose()

    @classmethod
    def tearDownClass(cls):
        asyncio.run(cls.drop_tables())
        cls.temp_db.close()
