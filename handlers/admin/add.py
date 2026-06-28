"""Admin panel — Add Restaurant FSM."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from constants import (
    CB_ADMIN_ADD,
    CB_ADMIN_CONFIRM_NO,
    CB_ADMIN_CONFIRM_YES,
    CB_ADMIN_DELIVERY_NO,
    CB_ADMIN_DELIVERY_YES,
    CB_ADMIN_STATE_PREFIX,
    MSG_ADMIN_CHOOSE_STATE,
    MSG_ADMIN_ENTER_ADDRESS,
    MSG_ADMIN_ENTER_DELIVERY,
    MSG_ADMIN_ENTER_MAPS,
    MSG_ADMIN_ENTER_NAME,
    MSG_ADMIN_ENTER_PHONE,
    MSG_ADMIN_ENTER_TELEGRAM,
    MSG_ADMIN_WELCOME,
)
from data.restaurants import RESTAURANTS, Restaurant
from keyboards.admin_kb import (
    get_admin_main_keyboard,
    get_admin_states_keyboard,
    get_confirm_keyboard,
    get_delivery_keyboard,
)
from states.admin_states import AddRestaurantFSM

logger = logging.getLogger(__name__)
router = Router(name=__name__)


# ---------------------------------------------------------------------------
# Step 1 — choose state
# ---------------------------------------------------------------------------

@router.callback_query(F.data == CB_ADMIN_ADD)
async def on_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Launch the Add Restaurant FSM."""
    await state.set_state(AddRestaurantFSM.choose_state)
    await callback.message.edit_text(
        text=MSG_ADMIN_CHOOSE_STATE,
        reply_markup=get_admin_states_keyboard(CB_ADMIN_STATE_PREFIX),
    )
    await callback.answer()


@router.callback_query(AddRestaurantFSM.choose_state, F.data.startswith(CB_ADMIN_STATE_PREFIX))
async def on_add_state_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_state = callback.data.removeprefix(CB_ADMIN_STATE_PREFIX)
    await state.update_data(state=chosen_state)
    await state.set_state(AddRestaurantFSM.enter_name)
    await callback.message.edit_text(text=MSG_ADMIN_ENTER_NAME)
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 2 — name
# ---------------------------------------------------------------------------

@router.message(AddRestaurantFSM.enter_name)
async def on_add_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    await state.set_state(AddRestaurantFSM.enter_phone)
    await message.answer(text=MSG_ADMIN_ENTER_PHONE)


# ---------------------------------------------------------------------------
# Step 3 — phone
# ---------------------------------------------------------------------------

@router.message(AddRestaurantFSM.enter_phone)
async def on_add_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.text.strip())
    await state.set_state(AddRestaurantFSM.enter_address)
    await message.answer(text=MSG_ADMIN_ENTER_ADDRESS)


# ---------------------------------------------------------------------------
# Step 4 — address
# ---------------------------------------------------------------------------

@router.message(AddRestaurantFSM.enter_address)
async def on_add_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text.strip())
    await state.set_state(AddRestaurantFSM.choose_delivery)
    await message.answer(text=MSG_ADMIN_ENTER_DELIVERY, reply_markup=get_delivery_keyboard())


# ---------------------------------------------------------------------------
# Step 5 — delivery
# ---------------------------------------------------------------------------

@router.callback_query(AddRestaurantFSM.choose_delivery, F.data == CB_ADMIN_DELIVERY_YES)
async def on_add_delivery_yes(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(delivery=True)
    await state.set_state(AddRestaurantFSM.enter_telegram)
    await callback.message.edit_text(text=MSG_ADMIN_ENTER_TELEGRAM)
    await callback.answer()


@router.callback_query(AddRestaurantFSM.choose_delivery, F.data == CB_ADMIN_DELIVERY_NO)
async def on_add_delivery_no(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(delivery=False)
    await state.set_state(AddRestaurantFSM.enter_telegram)
    await callback.message.edit_text(text=MSG_ADMIN_ENTER_TELEGRAM)
    await callback.answer()


# ---------------------------------------------------------------------------
# Step 6 — telegram link
# ---------------------------------------------------------------------------

@router.message(AddRestaurantFSM.enter_telegram)
async def on_add_telegram(message: Message, state: FSMContext) -> None:
    raw = message.text.strip()
    await state.update_data(telegram="" if raw == "-" else raw)
    await state.set_state(AddRestaurantFSM.enter_maps)
    await message.answer(text=MSG_ADMIN_ENTER_MAPS)


# ---------------------------------------------------------------------------
# Step 7 — maps link
# ---------------------------------------------------------------------------

@router.message(AddRestaurantFSM.enter_maps)
async def on_add_maps(message: Message, state: FSMContext) -> None:
    await state.update_data(maps=message.text.strip())
    data = await state.get_data()
    await state.set_state(AddRestaurantFSM.confirm)

    delivery_label = "✅ Yes" if data["delivery"] else "❌ No"
    preview = (
        f"📋 <b>Please confirm the new restaurant:</b>\n\n"
        f"📍 State: <b>{data['state']}</b>\n"
        f"🍽 Name: <b>{data['name']}</b>\n"
        f"📞 Phone: {data['phone']}\n"
        f"🏠 Address: {data['address']}\n"
        f"🚚 Delivery: {delivery_label}\n"
        f"📱 Telegram: {data.get('telegram') or '—'}\n"
        f"🗺 Maps: {data['maps']}"
    )
    await message.answer(text=preview, reply_markup=get_confirm_keyboard())


# ---------------------------------------------------------------------------
# Step 8 — confirm
# ---------------------------------------------------------------------------

@router.callback_query(AddRestaurantFSM.confirm, F.data == CB_ADMIN_CONFIRM_YES)
async def on_add_confirm_yes(callback: CallbackQuery, state: FSMContext) -> None:
    """Persist the new restaurant into RESTAURANTS."""
    data = await state.get_data()
    await state.clear()

    new_restaurant: Restaurant = {
        "name": data["name"],
        "phone": data["phone"],
        "address": data["address"],
        "delivery": data["delivery"],
        "telegram": data.get("telegram", ""),
        "maps": data["maps"],
    }
    RESTAURANTS.setdefault(data["state"], []).append(new_restaurant)
    from data.restaurants import save
    save()
    
    logger.info(
        "Restaurant added: %r to state=%r by user_id=%s",
        new_restaurant["name"],
        data["state"],
        callback.from_user.id,
    )

    await callback.message.edit_text(
        text=(
            f"✅ <b>{new_restaurant['name']}</b> has been added "
            f"to <b>{data['state']}</b>!\n\n{MSG_ADMIN_WELCOME}"
        ),
        reply_markup=get_admin_main_keyboard(),
    )
    await callback.answer()


@router.callback_query(AddRestaurantFSM.confirm, F.data == CB_ADMIN_CONFIRM_NO)
async def on_add_confirm_no(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel the add flow."""
    await state.clear()
    await callback.message.edit_text(
        text=f"❌ Cancelled.\n\n{MSG_ADMIN_WELCOME}",
        reply_markup=get_admin_main_keyboard(),
    )
    await callback.answer()