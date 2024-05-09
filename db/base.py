from typing import Self, TypeVar

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()
metadata = MetaData()


class OrmModel(Base):
    __abstract__ = True


class DBConnection:
    _instance = None

    engine: AsyncEngine
    async_session_ctx: sessionmaker

    def __new__(cls, *args, **kwargs):
        new_instance = super().__new__(cls)
        if cls._instance is None:
            cls._instance = new_instance
        return new_instance

    @classmethod
    def instance(cls) -> Self:
        return cls._instance

    def __init__(self, url: str | None = None):
        self.url = url
        self.engine = create_async_engine(self.url, poolclass=NullPool)
        self.async_session_ctx = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)  # noqa

    @classmethod
    def session(cls) -> AsyncSession:
        return cls.instance().async_session_ctx()
