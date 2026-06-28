"""Handler for state search by text input."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import (
    BTN_BACK_TO_STATES,
    CB_BACK_TO_STATES,
    CB_SEARCH,
    CB_SEARCH_RESULT_PREFIX,
    CB_STATE_PREFIX,
    MSG_SEARCH_NO_RESULTS,
    MSG_SEARCH_PROMPT,
    MSG_WELCOME,
)
from data.restaurants import RESTAURANTS
from keyboards.states_kb import get_states_keyboard
from states.admin_states import SearchFSM

logger = logging.getLogger(__name__)
router = Router(name=__name__)


def _find_states(query: str) -> list[str]:
    """Return states whose names contain the query (case-insensitive)."""
    q = query.strip().lower()
    return [s for s in RESTAURANTS if q in s.lower()]


def _build_results_keyboard(states: list[str]):
    """Keyboard with one button per matching state + Back button."""
    builder = InlineKeyboardBuilder()
    for state in states:
        builder.button(
            text=state,
            callback_data=f"{CB_SEARCH_RESULT_PREFIX}{state}",
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text=BTN_BACK_TO_STATES, callback_data=CB_BACK_TO_STATES)
    )
    return builder.as_markup()


# ---------------------------------------------------------------------------
# Entry — user pressed 🔍 Search
# ---------------------------------------------------------------------------

@router.callback_query(F.data == CB_SEARCH)
async def on_search_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Ask the user to type a state name."""
    await state.set_state(SearchFSM.waiting_for_query)
    await callback.message.edit_text(text=MSG_SEARCH_PROMPT)
    await callback.answer()


# ---------------------------------------------------------------------------
# User typed something while in search mode
# ---------------------------------------------------------------------------

@router.message(SearchFSM.waiting_for_query)
async def on_search_query(message: Message, state: FSMContext) -> None:
    """Search and show results or a no-results message."""
    query = message.text.strip() if message.text else ""
    logger.debug("Search query=%r user_id=%s", query, message.from_user.id)

    matches = _find_states(query)
    await state.clear()

    if not matches:
        # No results — send message and show back button
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text=BTN_BACK_TO_STATES, callback_data=CB_BACK_TO_STATES)
        )
        await message.answer(
            text=MSG_SEARCH_NO_RESULTS,
            reply_markup=builder.as_markup(),
        )
        return

    if len(matches) == 1:
        # Only one match — jump straight to it by simulating state selection
        # We reuse CB_SEARCH_RESULT_PREFIX to keep routing clean
        await message.answer(
            text=f"✅ Found: <b>{matches[0]}</b>",
            reply_markup=_build_results_keyboard(matches),
        )
        return

    await message.answer(
        text=f"🔍 Found <b>{len(matches)}</b> state(s) matching <code>{query}</code>:",
        reply_markup=_build_results_keyboard(matches),
    )


# ---------------------------------------------------------------------------
# User tapped a result button
# ---------------------------------------------------------------------------

@router.callback_query(F.data.startswith(CB_SEARCH_RESULT_PREFIX))
async def on_search_result_chosen(callback: CallbackQuery) -> None:
    """Route the user to the chosen state — same flow as normal state selection."""
    state_name = callback.data.removeprefix(CB_SEARCH_RESULT_PREFIX)

    # Import here to avoid circular imports at module level
    from handlers.states_list import show_restaurants_for_state  # noqa: PLC0415
    await show_restaurants_for_state(callback, state_name)