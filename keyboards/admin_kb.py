"""All keyboards used exclusively by the admin panel."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import (
    BTN_ADD,
    BTN_BACK_ADMIN,
    BTN_CANCEL,
    BTN_CONFIRM,
    BTN_DELETE,
    BTN_EDIT,
    BTN_EXIT,
    BTN_LIST,
    BTN_NO,
    BTN_YES,
    CB_ADMIN_ADD,
    CB_ADMIN_BACK_MENU,
    CB_ADMIN_CONFIRM_NO,
    CB_ADMIN_CONFIRM_YES,
    CB_ADMIN_DEL_CONFIRM_PREFIX,
    CB_ADMIN_DEL_REST_PREFIX,
    CB_ADMIN_DEL_STATE_PREFIX,
    CB_ADMIN_DELIVERY_NO,
    CB_ADMIN_DELIVERY_YES,
    CB_ADMIN_DELETE,
    CB_ADMIN_EDIT,
    CB_ADMIN_EDIT_FIELD_PREFIX,
    CB_ADMIN_EDIT_SELECT_PREFIX,
    CB_ADMIN_EXIT,
    CB_ADMIN_LIST,
    CB_ADMIN_LIST_STATE_PREFIX,
    CB_ADMIN_STATE_PREFIX,
    EDIT_FIELDS,
)
from data.restaurants import RESTAURANTS, Restaurant
from keyboards.builder import build_inline_keyboard


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Admin panel main menu."""
    buttons: list[tuple[str, str]] = [
        (BTN_ADD, CB_ADMIN_ADD),
        (BTN_EDIT, CB_ADMIN_EDIT),
        (BTN_DELETE, CB_ADMIN_DELETE),
        (BTN_LIST, CB_ADMIN_LIST),
        (BTN_EXIT, CB_ADMIN_EXIT),
    ]
    return build_inline_keyboard(buttons, width=1)


# ---------------------------------------------------------------------------
# Shared: state picker (used by add / edit / delete / list)
# ---------------------------------------------------------------------------

def get_admin_states_keyboard(cb_prefix: str) -> InlineKeyboardMarkup:
    """Inline keyboard listing all states; callback = <prefix><state>."""
    builder = InlineKeyboardBuilder()
    for state in RESTAURANTS:
        builder.button(text=state, callback_data=f"{cb_prefix}{state}")
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text=BTN_BACK_ADMIN, callback_data=CB_ADMIN_BACK_MENU)
    )
    return builder.as_markup()


# ---------------------------------------------------------------------------
# Add flow
# ---------------------------------------------------------------------------

def get_delivery_keyboard() -> InlineKeyboardMarkup:
    """Yes / No delivery question."""
    return build_inline_keyboard(
        [(BTN_YES, CB_ADMIN_DELIVERY_YES), (BTN_NO, CB_ADMIN_DELIVERY_NO)],
        width=2,
    )


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Confirm / Cancel prompt."""
    return build_inline_keyboard(
        [(BTN_CONFIRM, CB_ADMIN_CONFIRM_YES), (BTN_CANCEL, CB_ADMIN_CONFIRM_NO)],
        width=2,
    )


# ---------------------------------------------------------------------------
# Edit flow
# ---------------------------------------------------------------------------

def get_admin_restaurants_keyboard(
    state: str,
    restaurants: list[Restaurant],
    cb_prefix: str,
) -> InlineKeyboardMarkup:
    """List restaurants for selection (edit or delete flow)."""
    builder = InlineKeyboardBuilder()
    for idx, r in enumerate(restaurants):
        builder.button(
            text=f"{idx + 1}. {r['name']}",
            callback_data=f"{cb_prefix}{state}:{idx}",
        )
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text=BTN_BACK_ADMIN, callback_data=CB_ADMIN_BACK_MENU)
    )
    return builder.as_markup()


def get_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """Which field to edit."""
    builder = InlineKeyboardBuilder()
    for field_key, field_label in EDIT_FIELDS.items():
        builder.button(
            text=field_label,
            callback_data=f"{CB_ADMIN_EDIT_FIELD_PREFIX}{field_key}",
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text=BTN_BACK_ADMIN, callback_data=CB_ADMIN_BACK_MENU)
    )
    return builder.as_markup()


def get_edit_delivery_keyboard() -> InlineKeyboardMarkup:
    """Delivery toggle for edit flow — reuses add-flow callback data."""
    return get_delivery_keyboard()


# ---------------------------------------------------------------------------
# Delete flow
# ---------------------------------------------------------------------------

def get_delete_confirm_keyboard(state: str, idx: int) -> InlineKeyboardMarkup:
    """Confirm deletion of a specific restaurant by index."""
    return build_inline_keyboard(
        [
            (BTN_CONFIRM, f"{CB_ADMIN_DEL_CONFIRM_PREFIX}{state}:{idx}"),
            (BTN_CANCEL, CB_ADMIN_BACK_MENU),
        ],
        width=2,
    )


# ---------------------------------------------------------------------------
# List flow
# ---------------------------------------------------------------------------

def get_list_states_keyboard() -> InlineKeyboardMarkup:
    """State picker scoped to the list action."""
    return get_admin_states_keyboard(CB_ADMIN_LIST_STATE_PREFIX)


# ---------------------------------------------------------------------------
# Universal back button
# ---------------------------------------------------------------------------

def get_back_to_admin_keyboard() -> InlineKeyboardMarkup:
    """Single-button keyboard returning to the admin main menu."""
    return build_inline_keyboard([(BTN_BACK_ADMIN, CB_ADMIN_BACK_MENU)], width=1)