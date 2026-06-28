"""FSM state groups."""

from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class AddRestaurantFSM(StatesGroup):
    choose_state = State()
    enter_name = State()
    enter_phone = State()
    enter_address = State()
    choose_delivery = State()
    enter_telegram = State()
    enter_maps = State()
    confirm = State()


class EditRestaurantFSM(StatesGroup):
    choose_state = State()
    choose_restaurant = State()
    choose_field = State()
    enter_value = State()
    confirm = State()


class DeleteRestaurantFSM(StatesGroup):
    choose_state = State()
    choose_restaurant = State()
    confirm = State()


# NEW — search FSM
class SearchFSM(StatesGroup):
    """User types a state name, bot returns matching states."""
    waiting_for_query = State()