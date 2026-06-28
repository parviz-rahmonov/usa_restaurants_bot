"""Admin-access filter."""

from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class IsAdminFilter(BaseFilter):
    """Pass only if the acting user is listed in admin_ids.

    Works for both Message and CallbackQuery updates so it can be
    applied uniformly across all admin handlers.
    """

    def __init__(self, admin_ids: frozenset[int]) -> None:
        self._admin_ids = admin_ids

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        user = update.from_user
        return user is not None and user.id in self._admin_ids