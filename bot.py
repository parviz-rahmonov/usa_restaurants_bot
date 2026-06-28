"""Application entry point."""

from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import TelegramObject

from config import Settings, get_settings
from filters.chat_type import ChatTypeFilter
from handlers import restaurants, start, states_list, search  # ← search added
from handlers.admin import menu as admin_menu
from handlers.admin import add as admin_add
from handlers.admin import edit as admin_edit
from handlers.admin import delete as admin_delete
from handlers.admin import view as admin_view

logger = logging.getLogger(__name__)

_ALLOWED_CHAT_TYPES: list[str] = ["private", "group", "supergroup"]


class AdminMiddleware(BaseMiddleware):
    """Inject ``is_admin`` flag into handler data for every update."""

    def __init__(self, admin_ids: frozenset[int]) -> None:
        self._admin_ids = admin_ids

    async def __call__(self, handler, event: TelegramObject, data: dict) -> None:
        user = data.get("event_from_user")
        data["is_admin"] = user is not None and user.id in self._admin_ids
        await handler(event, data)


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


def _build_dispatcher(settings: Settings) -> Dispatcher:
    dp = Dispatcher()

    dp.update.middleware(AdminMiddleware(settings.admin_ids))
    dp.message.filter(ChatTypeFilter(_ALLOWED_CHAT_TYPES))

    # Public routers
    dp.include_router(search.router)       # ← search BEFORE states_list
    dp.include_router(start.router)
    dp.include_router(states_list.router)
    dp.include_router(restaurants.router)

    # Admin routers
    dp.include_router(admin_add.router)
    dp.include_router(admin_edit.router)
    dp.include_router(admin_delete.router)
    dp.include_router(admin_view.router)
    dp.include_router(admin_menu.router)

    return dp


async def main() -> None:
    _setup_logging()
    settings = get_settings()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = _build_dispatcher(settings)

    logger.info("Bot is starting…")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot stopped. Session closed.")


if __name__ == "__main__":
    asyncio.run(main())