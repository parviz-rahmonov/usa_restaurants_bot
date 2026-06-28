"""Handler for the /start command."""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from constants import MSG_WELCOME
from keyboards.states_kb import get_states_keyboard

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Send the welcome message with the states keyboard."""
    logger.debug("cmd_start: user_id=%s", message.from_user.id)
    await message.answer(text=MSG_WELCOME, reply_markup=get_states_keyboard())