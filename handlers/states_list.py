"""Handlers for states-selection, pagination and back-navigation."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from constants import (
    CB_BACK_TO_STATES,
    CB_PAGE_PREFIX,
    CB_STATE_PREFIX,
    MSG_NO_RESTAURANTS,
    MSG_WELCOME,
)
from data.restaurants import RESTAURANTS
from keyboards.restaurants_kb import get_restaurants_keyboard
from keyboards.states_kb import get_states_keyboard
from utils.formatters import format_restaurants_message

logger = logging.getLogger(__name__)
router = Router(name=__name__)


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

@router.callback_query(F.data.startswith(CB_PAGE_PREFIX))
async def on_page_change(callback: CallbackQuery) -> None:
    """Switch to a different page of states."""
    page = int(callback.data.removeprefix(CB_PAGE_PREFIX))
    logger.debug("Page change: page=%d user_id=%s", page, callback.from_user.id)
    await callback.message.edit_text(
        text=MSG_WELCOME,
        reply_markup=get_states_keyboard(page),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Shared logic — used by normal state selection AND by search results
# ---------------------------------------------------------------------------

async def show_restaurants_for_state(callback: CallbackQuery, state: str) -> None:
    """Display all restaurants for the given state.

    Reusable by any handler that already knows the state name
    (normal selection, search results, etc.) — avoids mutating
    the frozen CallbackQuery object.
    """
    logger.debug("State selected: %r  user_id=%s", state, callback.from_user.id)

    restaurants = RESTAURANTS.get(state)
    if not restaurants:
        await callback.answer(MSG_NO_RESTAURANTS, show_alert=True)
        return

    await callback.message.edit_text(
        text=format_restaurants_message("🏙 Restaurants in", state, restaurants),
        reply_markup=get_restaurants_keyboard(state, restaurants),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# State selected (entry point for the normal "pick from list" flow)
# ---------------------------------------------------------------------------

@router.callback_query(F.data.startswith(CB_STATE_PREFIX))
async def on_state_selected(callback: CallbackQuery) -> None:
    """Entry point for the normal 'pick a state from the list' flow."""
    state: str = callback.data.removeprefix(CB_STATE_PREFIX)
    await show_restaurants_for_state(callback, state)


# ---------------------------------------------------------------------------
# Back to states
# ---------------------------------------------------------------------------

@router.callback_query(F.data == CB_BACK_TO_STATES)
async def on_back_to_states(callback: CallbackQuery) -> None:
    """Return to the first page of states."""
    await callback.message.edit_text(
        text=MSG_WELCOME,
        reply_markup=get_states_keyboard(page=0),
    )
    await callback.answer()