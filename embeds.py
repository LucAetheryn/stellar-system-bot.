"""
Stellar System V2 — Embed Helpers
Centralised factory functions for consistent embed styling across all cogs.
"""

from __future__ import annotations

import traceback
from datetime import datetime

import discord

from utils.config import BOT_COLOR


def success(title: str, description: str = "") -> discord.Embed:
    """Green success embed."""
    return discord.Embed(
        title=f"✅  {title}",
        description=description,
        color=0x57F287,
        timestamp=datetime.utcnow(),
    )


def error(title: str, description: str = "") -> discord.Embed:
    """Red error embed."""
    return discord.Embed(
        title=f"❌  {title}",
        description=description,
        color=0xFF5555,
        timestamp=datetime.utcnow(),
    )


def info(title: str, description: str = "") -> discord.Embed:
    """Brand-purple informational embed."""
    return discord.Embed(
        title=title,
        description=description,
        color=BOT_COLOR,
        timestamp=datetime.utcnow(),
    )


def warning(title: str, description: str = "") -> discord.Embed:
    """Yellow warning embed."""
    return discord.Embed(
        title=f"⚠️  {title}",
        description=description,
        color=0xFEE75C,
        timestamp=datetime.utcnow(),
    )


def exception_embed(exc: Exception) -> discord.Embed:
    """
    Compact error embed shown to the user when an unhandled exception occurs.
    The full traceback is logged separately.
    """
    embed = discord.Embed(
        title="💥  An Unexpected Error Occurred",
        description=(
            "Something went wrong while processing your request.\n"
            "The error has been logged and will be reviewed."
        ),
        color=0xFF5555,
        timestamp=datetime.utcnow(),
    )
    embed.add_field(name="Error", value=f"```{type(exc).__name__}: {exc}```", inline=False)
    return embed
