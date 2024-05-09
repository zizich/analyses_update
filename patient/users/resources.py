from patient.users.dto import UserData
from patient.users.models import User
from utils.errors import ValidationError
from utils.resources import BaseResource


class UserResource(BaseResource):
    model = User

    @classmethod
    async def validate(cls, session, data: UserData) -> None:
        if await cls.exists(session=session, phone=int(data.phone)):
            raise ValidationError('Пользователь с таким номером телефона уже существует.')
