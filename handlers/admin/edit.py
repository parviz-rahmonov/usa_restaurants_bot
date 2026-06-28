"""Admin panel — Edit Restaurant FSM."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from constants import (
    CB_ADMIN_CONFIRM_NO,
    CB_ADMIN_CONFIRM_YES,
    CB_ADMIN_DELIVERY_NO,
    CB_ADMIN_DELIVERY_YES,
    CB_ADMIN_EDIT,
    CB_ADMIN_EDIT_FIELD_PREFIX,
    CB_ADMIN_EDIT_SELECT_PREFIX,
    EDIT_FIELDS,
    MSG_ADMIN_CHOOSE_EDIT_STATE,
    MSG_ADMIN_WELCOME,
)
from data.restaurants import RESTAURANTS
from keyboards.admin_kb import (
    get_admin_main_keyboard,
    get_admin_restaurants_keyboard,
    get_admin_states_keyboard,
    get_confirm_keyboard,
    get_edit_delivery_keyboard,
    get_edit_fields_keyboard,
)
from states.admin_states import EditRestaurantFSM

logger = logging.getLogger(__name__)
router = Router(name=__name__)

_DELIVERY_STATES = {CB_ADMIN_DELIVERY_YES: True, CB_ADMIN_DELIVERY_NO: False}


# ---------------------------------------------------------------------------
# Step 1 — choose state
# ---------------------------------------------------------------------------

@router.callback_query(F.data == CB_ADMIN_EDIT)
async def on_edit_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditRestaurantFSM.choose_state)
    await callback.message.edit_text(
        text=MSG_ADMIN_CHOOSE_EDIT_STATE,
        reply_markup=get_admin_states_keyboard(CB_ADMIN_EDIT_SELECT_PREFIX),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 2 — choose restaurant
# ---------------------------------------------------------------------------

@router.callback_query(
    EditRestaurantFSM.choose_state,
    F.data.startswith(CB_ADMIN_EDIT_SELECT_PREFIX),
)
async def on_edit_state_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    # prefix here is just the state name portion after "adm_edit_sel:"
    chosen_state = callback.data.removeprefix(CB_ADMIN_EDIT_SELECT_PREFIX)
    restaurants = RESTAURANTS.get(chosen_state, [])
    if not restaurants:
        await callback.answer("No restaurants in this state.", show_alert=True)
        return

    await state.update_data(state=chosen_state)
    await state.set_state(EditRestaurantFSM.choose_restaurant)
    await callback.message.edit_text(
        text=f"Select a restaurant to edit in <b>{chosen_state}</b>:",
        reply_markup=get_admin_restaurants_keyboard(
            chosen_state, restaurants, CB_ADMIN_EDIT_SELECT_PREFIX + "rest:"
        ),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 3 — choose field
# ---------------------------------------------------------------------------

@router.callback_query(
    EditRestaurantFSM.choose_restaurant,
    F.data.startswith(CB_ADMIN_EDIT_SELECT_PREFIX + "rest:"),
)
async def on_edit_restaurant_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    # callback.data = "adm_edit_sel:rest:<state>:<idx>"
    raw = callback.data.removeprefix(CB_ADMIN_EDIT_SELECT_PREFIX + "rest:")
    chosen_state, idx_str = raw.rsplit(":", 1)
    idx = int(idx_str)

    await state.update_data(state=chosen_state, restaurant_idx=idx)
    await state.set_state(EditRestaurantFSM.choose_field)

    restaurant = RESTAURANTS[chosen_state][idx]
    await callback.message.edit_text(
        text=f"Editing <b>{restaurant['name']}</b>.\nChoose a field to update:",
        reply_markup=get_edit_fields_keyboard(),
    )
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 4 — enter new value
# ---------------------------------------------------------------------------

@router.callback_query(
    EditRestaurantFSM.choose_field,
    F.data.startswith(CB_ADMIN_EDIT_FIELD_PREFIX),
)
async def on_edit_field_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    field = callback.data.removeprefix(CB_ADMIN_EDIT_FIELD_PREFIX)
    await state.update_data(field=field)

    if field == "delivery":
        await state.set_state(EditRestaurantFSM.enter_value)
        await callback.message.edit_text(
            text="Update delivery status:",
            reply_markup=get_edit_delivery_keyboard(),
        )
    else:
        label = EDIT_FIELDS.get(field, field)
        await state.set_state(EditRestaurantFSM.enter_value)
        await callback.message.edit_text(
            text=f"Enter new value for <b>{label}</b>:"
        )
    await callback.answer()


@router.callback_query(
    EditRestaurantFSM.enter_value,
    F.data.in_({CB_ADMIN_DELIVERY_YES, CB_ADMIN_DELIVERY_NO}),
)
async def on_edit_delivery_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle delivery toggle inside edit flow."""
    new_value = _DELIVERY_STATES[callback.data]
    await _show_edit_confirm(callback, state, new_value)
    await callback.answer()


@router.message(EditRestaurantFSM.enter_value)
async def on_edit_value_entered(message: Message, state: FSMContext) -> None:
    await _show_edit_confirm(message, state, message.text.strip())


async def _show_edit_confirm(
    update: Message | CallbackQuery,
    state: FSMContext,
    new_value: str | bool,
) -> None:
    await state.update_data(new_value=new_value)
    await state.set_state(EditRestaurantFSM.confirm)

    data = await state.get_data()
    field_label = EDIT_FIELDS.get(data["field"], data["field"])
    display = "✅ Yes" if new_value is True else ("❌ No" if new_value is False else new_value)

    text = (
        f"📝 <b>Confirm edit</b>\n\n"
        f"Restaurant: <b>{RESTAURANTS[data['state']][data['restaurant_idx']]['name']}</b>\n"
        f"Field: <b>{field_label}</b>\n"
        f"New value: <b>{display}</b>"
    )
    msg = update if isinstance(update, Message) else update.message
    await msg.answer(text=text, reply_markup=get_confirm_keyboard())


# ---------------------------------------------------------------------------
# Step 5 — confirm
# ---------------------------------------------------------------------------

@router.callback_query(EditRestaurantFSM.confirm, F.data == CB_ADMIN_CONFIRM_YES)
async def on_edit_confirm_yes(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    restaurant = RESTAURANTS[data["state"]][data["restaurant_idx"]]
    restaurant[data["field"]] = data["new_value"]
    from data.restaurants import save
    save()  # type: ignore[literal-required]

    logger.info(
        "Restaurant edited: %r field=%r user_id=%s",
        restaurant["name"],
        data["field"],
        callback.from_user.id,
    )
    await callback.message.edit_text(
        text=f"✅ <b>{restaurant['name']}</b> updated!\n\n{MSG_ADMIN_WELCOME}",
        reply_markup=get_admin_main_keyboard(),
    )
    await callback.answer()


@router.callback_query(EditRestaurantFSM.confirm, F.data == CB_ADMIN_CONFIRM_NO)
async def on_edit_confirm_no(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        text=f"❌ Edit cancelled.\n\n{MSG_ADMIN_WELCOME}",
        reply_markup=get_admin_main_keyboard(),
    )
    await callback.answer()