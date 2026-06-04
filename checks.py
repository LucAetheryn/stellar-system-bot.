"""
Stellar System V2 — Custom Permission Checks
Provides reusable app_commands.check decorators for slash commands.
"""

import discord
from discord import app_commands

from utils.config import OWNER_ID
from utils.logger import log


def is_admin():
    """Check that the invoking member has administrator permission."""

    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.guild_permissions.administrator:  # type: ignore[union-attr]
            return True
        await interaction.response.send_message(
            embed=_no_permission_embed("Administrator"),
            ephemeral=True,
        )
        return False

    return app_commands.check(predicate)


def is_moderator():
    """Check for Kick Members or Administrator permission."""

    async def predicate(interaction: discord.Interaction) -> bool:
        perms: discord.Permissions = interaction.user.guild_permissions  # type: ignore[union-attr]
        if perms.administrator or perms.kick_members:
            return True
        await interaction.response.send_message(
            embed=_no_permission_embed("Kick Members or Administrator"),
            ephemeral=True,
        )
        return False

    return app_commands.check(predicate)


def is_owner():
    """Restrict to the bot owner defined in OWNER_ID env var."""

    async def predicate(interaction: discord.Interaction) -> bool:
        if OWNER_ID and interaction.user.id == OWNER_ID:
            return True
        await interaction.response.send_message(
            embed=_no_permission_embed("Bot Owner"),
            ephemeral=True,
        )
        return False

    return app_commands.check(predicate)


def _no_permission_embed(required: str) -> discord.Embed:
    embed = discord.Embed(
        title="⛔ Access Denied",
        description=f"You need the **{required}** permission to use this command.",
        color=0xFF5555,
    )
    return embed
