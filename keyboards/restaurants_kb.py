"""Keyboard for the public restaurant-detail screen."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import (
    BTN_BACK_TO_STATES,
    BTN_DELIVERY_ONLY,
    BTN_SHOW_ALL,
    CB_BACK_TO_STATES,
    CB_DELIVERY_ALL_PREFIX,
    CB_DELIVERY_ONLY_PREFIX,
)

if TYPE_CHECKING:
    from data.restaurants import Restaurant


def get_restaurants_keyboard(
    state: str,
    restaurants: list[Restaurant],
    *,
    delivery_only: bool = False,
) -> InlineKeyboardMarkup:
    """Build the keyboard shown alongside a restaurant listing."""
    builder = InlineKeyboardBuilder()

    for restaurant in restaurants:
        row: list[InlineKeyboardButton] = []
        if restaurant["telegram"]:
            row.append(
                InlineKeyboardButton(
                    text=f"📱 {restaurant['name']} — Telegram",
                    url=restaurant["telegram"],
                )
            )
        row.append(
            InlineKeyboardButton(
                text=f"🗺 {restaurant['name']} — Maps",
                url=restaurant["maps"],
            )
        )
        builder.row(*row)

    toggle_text = BTN_SHOW_ALL if delivery_only else BTN_DELIVERY_ONLY
    toggle_cb = (
        f"{CB_DELIVERY_ALL_PREFIX}{state}"
        if delivery_only
        else f"{CB_DELIVERY_ONLY_PREFIX}{state}"
    )
    builder.row(
        InlineKeyboardButton(text=toggle_text, callback_data=toggle_cb),
        InlineKeyboardButton(text=BTN_BACK_TO_STATES, callback_data=CB_BACK_TO_STATES),
    )
    return builder.as_markup()