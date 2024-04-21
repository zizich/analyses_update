from aiogram.dispatcher.event.handler import CallbackType
from aiogram.types import BotCommand

from chat_bots.telegram import UserCase, Routes
from chat_bots.telegram.patient import commands
from chat_bots.telegram.patient.usercases import NewPatient


class PatientRoutes(Routes):
    commands: dict[CallbackType, BotCommand] = {
        commands.start:                                               BotCommand(command='start', description='Запуск бота'),  # noqa
        commands.cancel:                                                BotCommand(command='cancel', description='Отменить'),  # noqa
        commands.echo:                                                         BotCommand(command='echo', description='Эхо'),  # noqa
    }

    user_cases: dict[UserCase, BotCommand] = {
        NewPatient:                                                BotCommand(command='register', description='Регистрация'),  # noqa
    }
