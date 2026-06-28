"""Text formatting utilities — pure functions, no I/O."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.restaurants import Restaurant


def format_restaurant_card(restaurant: Restaurant) -> str:
    """Return an HTML-formatted card for a single restaurant."""
    delivery_label = "✅ Yes" if restaurant["delivery"] else "❌ No"
    return (
        f"<b>🍽 {restaurant['name']}</b>\n"
        f"📞 {restaurant['phone']}\n"
        f"📍 {restaurant['address']}\n"
        f"🚚 Delivery: {delivery_label}"
    )


def format_restaurants_message(
    header: str,
    state: str,
    restaurants: list[Restaurant],
) -> str:
    """Return a full message with a heading and individual restaurant cards."""
    heading = f"{header} <b>{state}</b>"
    cards = "\n\n".join(format_restaurant_card(r) for r in restaurants)
    return f"{heading}\n\n{cards}"


def format_admin_restaurant_card(index: int, restaurant: Restaurant) -> str:
    """Return a numbered HTML card used in the admin view-list screen."""
    delivery_label = "✅ Yes" if restaurant["delivery"] else "❌ No"
    tg = restaurant["telegram"] or "—"
    return (
        f"<b>{index}. {restaurant['name']}</b>\n"
        f"📞 {restaurant['phone']}\n"
        f"📍 {restaurant['address']}\n"
        f"🚚 Delivery: {delivery_label}\n"
        f"📱 Telegram: {tg}\n"
        f"🗺 Maps: {restaurant['maps']}"
    )