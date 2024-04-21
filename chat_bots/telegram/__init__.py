import abc
from typing import Protocol

from aiogram import Router
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.types import BotCommand


class UserCase(abc.ABC):

    def __hash__(self):
        return hash(self.__name__)

    def __eq__(self, other):
        if not isinstance(other, UserCase):
            return False
        return other.__name__ == self.__name__

    class States(abc.ABC):
        ...

    @property
    @abc.abstractmethod
    def router(self) -> Router: ...

    @property
    @abc.abstractmethod
    def entrypoint(self, *args, **kwargs): ...


class Routes(Protocol):
    commands: dict[CallbackType, BotCommand]
    user_cases: dict[UserCase, BotCommand]
