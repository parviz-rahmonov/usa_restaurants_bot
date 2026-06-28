"""Application configuration.

Loads environment variables from a .env file and exposes them
as a validated, immutable Settings object.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH: Path = Path(__file__).parent / ".env"


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable application settings populated from environment variables."""

    bot_token: str
    admin_ids: frozenset[int] = field(default_factory=frozenset)


def get_settings() -> Settings:
    """Load .env and return a validated Settings instance.

    Raises:
        ValueError: If BOT_TOKEN is missing or empty.
    """
    load_dotenv(_ENV_PATH)

    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError(
            "BOT_TOKEN is not set. "
            "Copy .env.example to .env and fill in the value."
        )

    raw_ids = os.getenv("ADMIN_IDS", "")
    admin_ids: frozenset[int] = frozenset(
        int(aid.strip())
        for aid in raw_ids.split(",")
        if aid.strip().isdigit()
    )

    return Settings(bot_token=token, admin_ids=admin_ids)