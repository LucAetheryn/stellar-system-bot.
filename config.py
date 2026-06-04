"""
Stellar System V2 — Configuration Management
Loads and validates environment variables at import time.
"""

import os
import sys

from dotenv import load_dotenv

from utils.logger import log

load_dotenv()


def _require(key: str) -> str:
    """Return the value of an env var or abort with a clear message."""
    value = os.getenv(key)
    if not value:
        log.critical("Missing required environment variable: %s", key)
        sys.exit(1)
    return value


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default)


# ── Required ──────────────────────────────────────────────────────────────────
TOKEN: str = _require("TOKEN")
GUILD_ID: int = int(_require("GUILD_ID"))

# ── Optional ──────────────────────────────────────────────────────────────────
STAFF_ROLE_ID: int | None = (
    int(v) if (v := _optional("STAFF_ROLE_ID")) else None
)
OWNER_ID: int | None = (
    int(v) if (v := _optional("OWNER_ID")) else None
)

# ── Static constants ──────────────────────────────────────────────────────────
DATABASE_PATH: str = "data/stellar.db"
BOT_COLOR: int = 0xBB86FC
BOT_VERSION: str = "2.0.0"
BOT_NAME: str = "Stellar System V2"
