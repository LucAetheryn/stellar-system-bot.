"""
Stellar System V2 — Database Layer
Provides an async SQLite interface built on aiosqlite.
All public functions accept a guild_id and operate on a single shared DB file.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

import aiosqlite

from utils.config import DATABASE_PATH
from utils.logger import log

# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

async def init_db() -> None:
    """
    Ensure the database file and all tables exist.
    Reads schema.sql and executes it so this is idempotent on every startup.
    """
    os.makedirs(Path(DATABASE_PATH).parent, exist_ok=True)
    schema_path = Path(__file__).parent / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(schema)
        await db.commit()

    log.info("Database initialised at %s", DATABASE_PATH)


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

async def _fetchone(query: str, params: tuple = ()) -> dict[str, Any] | None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def _fetchall(query: str, params: tuple = ()) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def _execute(query: str, params: tuple = ()) -> int:
    """Execute a write query and return the lastrowid."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(query, params) as cur:
            await db.commit()
            return cur.lastrowid or 0


# ---------------------------------------------------------------------------
# guild_settings
# ---------------------------------------------------------------------------

async def get_setting(guild_id: int, key: str) -> str | None:
    row = await _fetchone(
        "SELECT value FROM guild_settings WHERE guild_id = ? AND key = ?",
        (guild_id, key),
    )
    return row["value"] if row else None


async def set_setting(guild_id: int, key: str, value: str) -> None:
    await _execute(
        "INSERT INTO guild_settings (guild_id, key, value) VALUES (?, ?, ?) "
        "ON CONFLICT(guild_id, key) DO UPDATE SET value = excluded.value",
        (guild_id, key, value),
    )


# ---------------------------------------------------------------------------
# welcome_channels
# ---------------------------------------------------------------------------

async def get_welcome_channel(guild_id: int) -> int | None:
    row = await _fetchone(
        "SELECT channel_id FROM welcome_channels WHERE guild_id = ?",
        (guild_id,),
    )
    return int(row["channel_id"]) if row else None


async def set_welcome_channel(guild_id: int, channel_id: int) -> None:
    await _execute(
        "INSERT INTO welcome_channels (guild_id, channel_id) VALUES (?, ?) "
        "ON CONFLICT(guild_id) DO UPDATE SET channel_id = excluded.channel_id",
        (guild_id, channel_id),
    )


# ---------------------------------------------------------------------------
# autoroles
# ---------------------------------------------------------------------------

async def add_autorole(guild_id: int, role_id: int) -> None:
    await _execute(
        "INSERT OR IGNORE INTO autoroles (guild_id, role_id) VALUES (?, ?)",
        (guild_id, role_id),
    )


async def remove_autorole(guild_id: int, role_id: int) -> None:
    await _execute(
        "DELETE FROM autoroles WHERE guild_id = ? AND role_id = ?",
        (guild_id, role_id),
    )


async def get_autoroles(guild_id: int) -> list[int]:
    rows = await _fetchall(
        "SELECT role_id FROM autoroles WHERE guild_id = ?",
        (guild_id,),
    )
    return [int(r["role_id"]) for r in rows]


# ---------------------------------------------------------------------------
# tickets
# ---------------------------------------------------------------------------

async def create_ticket(guild_id: int, channel_id: int, user_id: int) -> int:
    return await _execute(
        "INSERT INTO tickets (guild_id, channel_id, user_id) VALUES (?, ?, ?)",
        (guild_id, channel_id, user_id),
    )


async def get_ticket_by_channel(channel_id: int) -> dict[str, Any] | None:
    return await _fetchone(
        "SELECT * FROM tickets WHERE channel_id = ?",
        (channel_id,),
    )


async def get_open_ticket(guild_id: int, user_id: int) -> dict[str, Any] | None:
    return await _fetchone(
        "SELECT * FROM tickets WHERE guild_id = ? AND user_id = ? AND status = 'open'",
        (guild_id, user_id),
    )


async def close_ticket(channel_id: int) -> None:
    await _execute(
        "UPDATE tickets SET status = 'closed', closed_at = datetime('now') "
        "WHERE channel_id = ?",
        (channel_id,),
    )


async def delete_ticket(channel_id: int) -> None:
    await _execute(
        "UPDATE tickets SET status = 'deleted' WHERE channel_id = ?",
        (channel_id,),
    )


# ---------------------------------------------------------------------------
# warnings
# ---------------------------------------------------------------------------

async def add_warning(
    guild_id: int, user_id: int, moderator_id: int, reason: str
) -> int:
    return await _execute(
        "INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
        (guild_id, user_id, moderator_id, reason),
    )


async def get_warnings(guild_id: int, user_id: int) -> list[dict[str, Any]]:
    return await _fetchall(
        "SELECT * FROM warnings WHERE guild_id = ? AND user_id = ? ORDER BY created_at DESC",
        (guild_id, user_id),
    )


async def remove_warning(warn_id: int, guild_id: int) -> bool:
    """Returns True if a row was deleted."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "DELETE FROM warnings WHERE warn_id = ? AND guild_id = ?",
            (warn_id, guild_id),
        ) as cur:
            await db.commit()
            return cur.rowcount > 0


# ---------------------------------------------------------------------------
# log_channels
# ---------------------------------------------------------------------------

async def get_log_channel(guild_id: int) -> int | None:
    row = await _fetchone(
        "SELECT channel_id FROM log_channels WHERE guild_id = ?",
        (guild_id,),
    )
    return int(row["channel_id"]) if row else None


async def set_log_channel(guild_id: int, channel_id: int) -> None:
    await _execute(
        "INSERT INTO log_channels (guild_id, channel_id) VALUES (?, ?) "
        "ON CONFLICT(guild_id) DO UPDATE SET channel_id = excluded.channel_id",
        (guild_id, channel_id),
    )
