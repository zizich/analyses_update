from unittest.mock import AsyncMock, MagicMock


class Chat(MagicMock):
    ...


class Message(MagicMock):
    answer = AsyncMock()
