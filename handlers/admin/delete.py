"""Admin panel — Delete Restaurant FSM."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from constants import (
    CB_ADMIN_DEL_CONFIRM_PREFIX,
    CB_ADMIN_DEL_REST_PREFIX,
    CB_ADMIN_DEL_STATE_PREFIX,
    CB_ADMIN_DELETE,
    MSG_ADMIN_CHOOSE_DEL_STATE,
    MSG_ADMIN_WELCOME,
)
from data.restaurants import RESTAURANTS
from keyboards.admin_kb import (
    get_admin_main_keyboard,
    get_admin_restaurants_keyboard,
    get_admin_states_keyboard,
    get_delete_confirm_keyboard,
)
from states.admin_states import DeleteRestaurantFSM
from utils.formatters import format_admin_restaurant_card

logger = logging.getLogger(__name__)
router = Router(name=__name__)


# ---------------------------------------------------------------------------
# Step 1 — choose state
# ---------------------------------------------------------------------------

@router.callback_query(F.data == CB_ADMIN_DELETE)
async def on_delete_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DeleteRestaurantFSM.choose_state)
    await callback.message.edit_text(
        text=MSG_ADMIN_CHOOSE_DEL_STATE,
        reply_markup=get_admin_states_keyboard(CB_ADMIN_DEL_STATE_PREFIX),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 2 — choose restaurant
# ---------------------------------------------------------------------------

@router.callback_query(
    DeleteRestaurantFSM.choose_state,
    F.data.startswith(CB_ADMIN_DEL_STATE_PREFIX),
)
async def on_delete_state_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_state = callback.data.removeprefix(CB_ADMIN_DEL_STATE_PREFIX)
    restaurants = RESTAURANTS.get(chosen_state, [])
    if not restaurants:
        await callback.answer("No restaurants in this state.", show_alert=True)
        return

    await state.update_data(state=chosen_state)
    await state.set_state(DeleteRestaurantFSM.choose_restaurant)
    await callback.message.edit_text(
        text=f"Select a restaurant to <b>delete</b> in <b>{chosen_state}</b>:",
        reply_markup=get_admin_restaurants_keyboard(
            chosen_state, restaurants, CB_ADMIN_DEL_REST_PREFIX
        ),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 3 — confirm
# ---------------------------------------------------------------------------

@router.callback_query(
    DeleteRestaurantFSM.choose_restaurant,
    F.data.startswith(CB_ADMIN_DEL_REST_PREFIX),
)
async def on_delete_restaurant_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    raw = callback.data.removeprefix(CB_ADMIN_DEL_REST_PREFIX)
    chosen_state, idx_str = raw.rsplit(":", 1)
    idx = int(idx_str)

    restaurants = RESTAURANTS.get(chosen_state, [])
    if idx >= len(restaurants):
        await callback.answer("Restaurant not found.", show_alert=True)
        return

    await state.update_data(state=chosen_state, restaurant_idx=idx)
    await state.set_state(DeleteRestaurantFSM.confirm)

    card = format_admin_restaurant_card(idx + 1, restaurants[idx])
    await callback.message.edit_text(
        text=f"⚠️ Are you sure you want to delete this restaurant?\n\n{card}",
        reply_markup=get_delete_confirm_keyboard(chosen_state, idx),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 4 — execute deletion
# ---------------------------------------------------------------------------

@router.callback_query(
    DeleteRestaurantFSM.confirm,
    F.data.startswith(CB_ADMIN_DEL_CONFIRM_PREFIX),
)
async def on_delete_confirmed(callback: CallbackQuery, state: FSMContext) -> None:
    raw = callback.data.removeprefix(CB_ADMIN_DEL_CONFIRM_PREFIX)
    chosen_state, idx_str = raw.rsplit(":", 1)
    idx = int(idx_str)

    restaurants = RESTAURANTS.get(chosen_state, [])
    if idx >= len(restaurants):
        await callback.answer("Already deleted.", show_alert=True)
        await state.clear()
        return

    removed = restaurants.pop(idx)
    from data.restaurants import save
    save()
    await state.clear()

    logger.info(
        "Restaurant deleted: %r from state=%r by user_id=%s",
        removed["name"],
        chosen_state,
        callback.from_user.id,
    )
    await callback.message.edit_text(
        text=f"🗑 <b>{removed['name']}</b> has been deleted.\n\n{MSG_ADMIN_WELCOME}",
        reply_markup=get_admin_main_keyboard(),
    )
    await callback.answer()