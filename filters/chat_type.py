"""Chat-type guard filter."""

from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    """Allow messages only from the specified chat types."""

    def __init__(self, chat_types: list[str]) -> None:
        self._allowed: frozenset[str] = frozenset(chat_types)

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self._allowed