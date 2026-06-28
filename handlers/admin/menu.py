"""Admin panel — main menu and access guard."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from constants import (
    CB_ADMIN_BACK_MENU,
    CB_ADMIN_EXIT,
    MSG_ACCESS_DENIED,
    MSG_ADMIN_WELCOME,
)
from keyboards.admin_kb import get_admin_main_keyboard

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(Command("admin"))
async def cmd_admin(message: Message, is_admin: bool) -> None:
    """Entry point for /admin command.

    ``is_admin`` is injected by the middleware defined in bot.py via
    ``data["is_admin"]`` — see _AdminMiddleware.
    """
    if not is_admin:
        logger.warning("Access denied for user_id=%s", message.from_user.id)
        await message.answer(MSG_ACCESS_DENIED)
        return

    logger.debug("Admin panel opened by user_id=%s", message.from_user.id)
    await message.answer(text=MSG_ADMIN_WELCOME, reply_markup=get_admin_main_keyboard())


@router.callback_query(F.data == CB_ADMIN_BACK_MENU)
async def on_back_to_admin_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Return to admin main menu from any sub-screen, clearing FSM state."""
    await state.clear()
    await callback.message.edit_text(
        text=MSG_ADMIN_WELCOME,
        reply_markup=get_admin_main_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == CB_ADMIN_EXIT)
async def on_admin_exit(callback: CallbackQuery, state: FSMContext) -> None:
    """Close the admin panel."""
    await state.clear()
    await callback.message.edit_text("👋 Admin panel closed.")
    await callback.answer()