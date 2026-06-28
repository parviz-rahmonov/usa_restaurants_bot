"""Keyboard for the public states-selection screen with pagination."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import (
    BTN_NEXT_PAGE,
    BTN_PREV_PAGE,
    BTN_SEARCH,
    CB_PAGE_PREFIX,
    CB_SEARCH,
    CB_STATE_PREFIX,
    ITEMS_PER_PAGE,
    MSG_PAGE_INFO,
)
from data.restaurants import RESTAURANTS

_STATE_EMOJI: dict[str, str] = {
    "Alabama": "🌹", "Alaska": "🐻", "Arizona": "🌵", "Arkansas": "💎",
    "California": "🌴", "Colorado": "⛰️", "Connecticut": "🏛️", "Delaware": "🦅",
    "Florida": "☀️", "Georgia": "🍑", "Hawaii": "🌺", "Idaho": "🥔",
    "Illinois": "🌆", "Indiana": "🏎️", "Iowa": "🌽", "Kansas": "🌾",
    "Kentucky": "🐎", "Louisiana": "🎷", "Maine": "🦞", "Maryland": "🦀",
    "Massachusetts": "🫐", "Michigan": "🚗", "Minnesota": "❄️",
    "Mississippi": "🎸", "Missouri": "⚾", "Montana": "🦌", "Nebraska": "🌻",
    "Nevada": "🎰", "New Hampshire": "🍁", "New Jersey": "🗺️",
    "New Mexico": "🌶️", "New York": "🗽", "North Carolina": "🏖️",
    "North Dakota": "🌄", "Ohio": "🎡", "Oklahoma": "🌪️", "Oregon": "🌲",
    "Pennsylvania": "🔔", "Rhode Island": "⚓", "South Carolina": "🌴",
    "South Dakota": "🗿", "Tennessee": "🎵", "Texas": "🤠", "Utah": "🏜️",
    "Vermont": "🍂", "Virginia": "🌿", "Washington": "☕",
    "West Virginia": "⛰️", "Wisconsin": "🧀", "Wyoming": "🦬",
}
_DEFAULT_EMOJI = "📍"


def get_states_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    """Inline keyboard with paginated state buttons and a search button.

    Args:
        page: Zero-based page index.
    """
    all_states = list(RESTAURANTS.keys())
    total_pages = max(1, -(-len(all_states) // ITEMS_PER_PAGE))  # ceil division
    page = max(0, min(page, total_pages - 1))

    start = page * ITEMS_PER_PAGE
    page_states = all_states[start: start + ITEMS_PER_PAGE]

    builder = InlineKeyboardBuilder()

    # State buttons — 2 per row
    for state in page_states:
        emoji = _STATE_EMOJI.get(state, _DEFAULT_EMOJI)
        builder.button(
            text=f"{emoji} {state}",
            callback_data=f"{CB_STATE_PREFIX}{state}",
        )
    builder.adjust(2)

    # Pagination row
    nav_buttons: list[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text=BTN_PREV_PAGE, callback_data=f"{CB_PAGE_PREFIX}{page - 1}")
        )
    nav_buttons.append(
        InlineKeyboardButton(
            text=MSG_PAGE_INFO.format(page=page + 1, total=total_pages),
            callback_data="noop",  # non-functional, just shows info
        )
    )
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(text=BTN_NEXT_PAGE, callback_data=f"{CB_PAGE_PREFIX}{page + 1}")
        )
    builder.row(*nav_buttons)

    # Search button
    builder.row(InlineKeyboardButton(text=BTN_SEARCH, callback_data=CB_SEARCH))

    return builder.as_markup()