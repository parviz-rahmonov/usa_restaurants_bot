"""Low-level keyboard construction helper."""

from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_inline_keyboard(
    buttons: list[tuple[str, str]],
    width: int = 2,
) -> InlineKeyboardMarkup:
    """Build an inline keyboard from (text, callback_data) pairs."""
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)
    builder.adjust(width)
    return builder.as_markup()