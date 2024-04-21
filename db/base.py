from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


Base = declarative_base()
metadata = MetaData()


class DB:
    engine: AsyncEngine
    async_session_maker: sessionmaker

    def __init__(self, url: str):
        self.url = url
        self.engine = create_async_engine(self.url, poolclass=NullPool)
        self.async_session_maker = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def _get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

    def session(self):
        return self._get_async_session()
