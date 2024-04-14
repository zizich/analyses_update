from typing import TypeAlias

from aiogram import F
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.filters import Command

from adapters.telegram import handlers

Handler: TypeAlias = CallbackType
Filter: TypeAlias = CallbackType
Filters: TypeAlias = tuple[Filter, ...]


# Важно! Требуется сохранять очередность
routes: list[tuple[Handler, Filter | Filters]] = [
    (handlers.command_start_handler,                                                                  Command('start')),  # noqa
    (handlers.command_custom,                                                                        Command('custom')),  # noqa
    (handlers.callback_handler,                                                                   F.data == 'callback'),  # noqa
    (handlers.echo_handler,                                                                                           ),  # noqa
]
