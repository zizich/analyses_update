import functools

from sqlalchemy import select
from sqlalchemy.engine.result import ScalarResult

from db.base import DBConnection
from patient.users.dto import UserData
from patient.users.models import User
from utils.errors import ValidationError


class UserResource:
    model = User
    db = DBConnection

    @classmethod
    def _where_criteria(cls, **kwargs) -> tuple[bool, ...]:
        # tuple[bool] == tuple[_ColumnExpressionArgument]
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
    async def create(cls, user_data: UserData) -> None:
        async with cls.db.session() as session:

            if await cls.exists(session=session, phone=user_data.phone):
                raise ValidationError('Пользователь с таким номером телефона уже существует.')

            user = User(**user_data.model_dump())
            session.add(user)
            await session.commit()
