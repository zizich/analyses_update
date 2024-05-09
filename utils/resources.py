import functools
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine.result import ScalarResult

from db.base import OrmModel, DBConnection


class BaseResource:

    model: type[OrmModel]
    model_dto: type[BaseModel]
    db: DBConnection = DBConnection

    @classmethod
    def _where_criteria(cls, **kwargs) -> tuple[bool, ...]:
        attr = functools.partial(getattr, cls.model)
        return tuple(attr(name) == value for name, value in kwargs.items() if attr(name))

    @classmethod
    async def exists(cls, session, **kwargs) -> bool:
        query = select(cls.model).where(*cls._where_criteria(**kwargs))
        result = await session.execute(query)
        return True if result.scalars().one_or_none() else False

    @classmethod
    async def get(cls, **kwargs) -> ScalarResult:
        async with cls.db.session() as session:
            query = select(cls.model)
            if kwargs:
                query = query.where(*cls._where_criteria(**kwargs))
            result = await session.execute(query)
            return result.scalars()

    @classmethod
    async def validate(cls, session, data: 'model_dto') -> None:
        ...

    @classmethod
    async def create(cls, data: 'model_dto') -> None:
        async with cls.db.session() as session:
            await cls.validate(session, data)
            model_instance = cls.model(**data.model_dump())
            session.add(model_instance)
            await session.commit()
