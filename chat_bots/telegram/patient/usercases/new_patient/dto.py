import contextlib
from typing import Self, TypeAlias

from pydantic import (
    BaseModel,
    Field, field_validator,
)

from patient.users.dto import UserData

ErrMsg: TypeAlias = str


class ProfileDTO(BaseModel):
    __WARNING = 'Важно! Каждый из пунктов должен начинаться с новой строки, без знаков припинания в конце!\n'
    __HELP = (
        '1.ФИО\n'
        'Фамилия Имя Отчество должны быть указаны через пробел.\n'
        'Пример: Иванов Иван Иванович\n'
        '\n'
        '2.Номер телефона\n'
        'Номер телефона должен начинаться с цифры "8" и содержать 11 символов.\n'
        'Пример: 80000123456\n'
        '\n'
        '3.Адрес проживания\n'
        'Адрес проживания должен содержать (через запятую): Город, Название улицы, Номер дома, Номер квартиры.\n'
        'Пример: Сургут, Ленина, 1, 1\n'
    )

    full_name: str = Field(title='ФИО')
    # phone: int = Field(title='Номер телефона', min_length=11, max_length=11)
    phone: int = Field(title='Номер телефона')
    address: str = Field(title='Адрес проживания')

    def __str__(self):
        info = ''
        for field_name, field_info in self.model_fields.items():
            info += f'{field_info.title}: {getattr(self, field_name)}\n'
        return info

    @classmethod
    def help(cls) -> str:
        return cls.__HELP.default  # noqa pydantic add default

    @classmethod
    def warning(cls) -> str:
        return cls.__WARNING.default  # noqa pydantic add default

    @classmethod
    def parse_text(cls, text: str) -> tuple[Self | None, ErrMsg | None]:
        with contextlib.suppress(ValueError):
            full_name, phone, address = text.split('\n')
            return cls(full_name=full_name, phone=phone, address=address), None

        return None, 'Полученные данные введены некорректно.\n'

    def data_to_save(self) -> UserData:
        return UserData(**self.model_dump())

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, value):
        return value

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        return value

    @field_validator('address')
    @classmethod
    def validate_address(cls, value):
        return value
