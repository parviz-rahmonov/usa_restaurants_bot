"""Handlers for the delivery-filter toggle."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from constants import (
    CB_DELIVERY_ALL_PREFIX,
    CB_DELIVERY_ONLY_PREFIX,
    MSG_NO_DELIVERY,
    MSG_STATE_NOT_FOUND,
)
from data.restaurants import RESTAURANTS, Restaurant
from keyboards.restaurants_kb import get_restaurants_keyboard
from utils.formatters import format_restaurants_message

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(F.data.startswith(CB_DELIVERY_ONLY_PREFIX))
async def on_delivery_only(callback: CallbackQuery) -> None:
    """Filter to delivery-available restaurants only."""
    state: str = callback.data.removeprefix(CB_DELIVERY_ONLY_PREFIX)

    delivery_restaurants: list[Restaurant] = [
        r for r in RESTAURANTS.get(state, []) if r["delivery"]
    ]
    if not delivery_restaurants:
        await callback.answer(MSG_NO_DELIVERY, show_alert=True)
        return

    await callback.message.edit_text(
        text=format_restaurants_message(
            "🚚 Delivery restaurants in", state, delivery_restaurants
        ),
        reply_markup=get_restaurants_keyboard(
            state, delivery_restaurants, delivery_only=True
        ),
    )
    await callback.answer()


@router.callback_query(F.data.startswith(CB_DELIVERY_ALL_PREFIX))
async def on_delivery_all(callback: CallbackQuery) -> None:
    """Reset the delivery filter and show all restaurants."""
    state: str = callback.data.removeprefix(CB_DELIVERY_ALL_PREFIX)

    all_restaurants = RESTAURANTS.get(state, [])
    if not all_restaurants:
        await callback.answer(MSG_STATE_NOT_FOUND, show_alert=True)
        return

    await callback.message.edit_text(
        text=format_restaurants_message("🏙 Restaurants in", state, all_restaurants),
        reply_markup=get_restaurants_keyboard(
            state, all_restaurants, delivery_only=False
        ),
    )
    await callback.answer()