"""Admin panel — View Restaurants (read-only list)."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from constants import (
    CB_ADMIN_LIST,
    CB_ADMIN_LIST_STATE_PREFIX,
    MSG_ADMIN_CHOOSE_LIST_STATE,
)
from data.restaurants import RESTAURANTS
from keyboards.admin_kb import get_back_to_admin_keyboard, get_list_states_keyboard
from utils.formatters import format_admin_restaurant_card

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(F.data == CB_ADMIN_LIST)
async def on_list_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Show the state picker for the list view."""
    await state.clear()
    await callback.message.edit_text(
        text=MSG_ADMIN_CHOOSE_LIST_STATE,
        reply_markup=get_list_states_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith(CB_ADMIN_LIST_STATE_PREFIX))
async def on_list_state_chosen(callback: CallbackQuery) -> None:
    """Display all restaurants for the chosen state (admin view)."""
    chosen_state = callback.data.removeprefix(CB_ADMIN_LIST_STATE_PREFIX)
    restaurants = RESTAURANTS.get(chosen_state, [])

    if not restaurants:
        await callback.answer("No restaurants in this state.", show_alert=True)
        return

    cards = "\n\n".join(
        format_admin_restaurant_card(i + 1, r) for i, r in enumerate(restaurants)
    )
    await callback.message.edit_text(
        text=f"📋 <b>Restaurants in {chosen_state}</b> ({len(restaurants)} total)\n\n{cards}",
        reply_markup=get_back_to_admin_keyboard(),
    )
    await callback.answer()