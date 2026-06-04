"""
Stellar System V2 — Logging System Cog
Listens to Discord events and posts structured log embeds to a configured channel.
Commands: /setlog, /viewlog
"""

from __future__ import annotations

from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from database import database as db
from utils import embeds
from utils.checks import is_admin
from utils.logger import log


class LoggingCog(commands.Cog, name="Logging"):
    """Event logging — mirrors Discord events to a log channel."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── Internal helper ───────────────────────────────────────────────────────

    async def _get_log_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        channel_id = await db.get_log_channel(guild.id)
        if not channel_id:
            return None
        ch = guild.get_channel(channel_id)
        return ch if isinstance(ch, discord.TextChannel) else None

    async def _send_log(self, guild: discord.Guild, embed: discord.Embed) -> None:
        channel = await self._get_log_channel(guild)
        if channel:
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass

    # ── Slash command: /setlog ────────────────────────────────────────────────

    @app_commands.command(
        name="setlog",
        description="Set the channel where bot events will be logged. (Admin only)",
    )
    @app_commands.describe(channel="The text channel to send logs to.")
    @is_admin()
    async def setlog(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        await db.set_log_channel(interaction.guild_id, channel.id)  # type: ignore[arg-type]
        await interaction.response.send_message(
            embed=embeds.success(
                "Log Channel Set",
                f"All bot events will now be logged to {channel.mention}.",
            )
        )
        log.info(
            "Log channel set to #%s (%d) in guild %d by %s",
            channel.name,
            channel.id,
            interaction.guild_id,
            interaction.user,
        )

    # ── Slash command: /viewlog ───────────────────────────────────────────────

    @app_commands.command(name="viewlog", description="View the currently configured log channel.")
    @is_admin()
    async def viewlog(self, interaction: discord.Interaction) -> None:
        channel_id = await db.get_log_channel(interaction.guild_id)  # type: ignore[arg-type]
        if not channel_id:
            await interaction.response.send_message(
                embed=embeds.info("Log Channel", "No log channel is currently configured.\nUse `/setlog` to set one."),
                ephemeral=True,
            )
            return

        ch = interaction.guild.get_channel(channel_id) if interaction.guild else None  # type: ignore[union-attr]
        mention = ch.mention if ch else f"`{channel_id}` (channel not found)"
        await interaction.response.send_message(
            embed=embeds.info("Log Channel", f"Current log channel: {mention}"),
            ephemeral=True,
        )

    # ── Event: message delete ─────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return

        embed = discord.Embed(
            title="🗑️  Message Deleted",
            color=0xFF5555,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="Author", value=f"{message.author.mention} (`{message.author.id}`)", inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)  # type: ignore[union-attr]
        embed.add_field(
            name="Content",
            value=message.content[:1024] if message.content else "*No text content*",
            inline=False,
        )
        await self._send_log(message.guild, embed)

    # ── Event: message edit ───────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.author.bot or not before.guild or before.content == after.content:
            return

        embed = discord.Embed(
            title="✏️  Message Edited",
            color=0xFEE75C,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="Author", value=f"{before.author.mention} (`{before.author.id}`)", inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)  # type: ignore[union-attr]
        embed.add_field(name="Before", value=before.content[:512] or "*Empty*", inline=False)
        embed.add_field(name="After", value=after.content[:512] or "*Empty*", inline=False)
        embed.add_field(name="Jump", value=f"[View Message]({after.jump_url})", inline=False)
        await self._send_log(before.guild, embed)

    # ── Event: member join ────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        embed = discord.Embed(
            title="📥  Member Joined",
            description=f"{member.mention} joined the server.",
            color=0x57F287,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="User", value=f"{member} (`{member.id}`)", inline=True)
        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(member.created_at, style="R"),
            inline=True,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await self._send_log(member.guild, embed)

    # ── Event: member leave ───────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        embed = discord.Embed(
            title="📤  Member Left",
            description=f"**{member}** (`{member.id}`) has left or was removed.",
            color=0xFF5555,
            timestamp=datetime.now(timezone.utc),
        )
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        embed.add_field(
            name="Roles",
            value=" ".join(roles) if roles else "None",
            inline=False,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await self._send_log(member.guild, embed)

    # ── Event: member update (role changes) ───────────────────────────────────

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        added = [r for r in after.roles if r not in before.roles]
        removed = [r for r in before.roles if r not in after.roles]

        if not added and not removed:
            return

        embed = discord.Embed(
            title="🔄  Member Role Update",
            color=0xBB86FC,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="Member", value=f"{after.mention} (`{after.id}`)", inline=False)

        if added:
            embed.add_field(
                name="Roles Added",
                value=" ".join(r.mention for r in added),
                inline=True,
            )
        if removed:
            embed.add_field(
                name="Roles Removed",
                value=" ".join(r.mention for r in removed),
                inline=True,
            )

        await self._send_log(after.guild, embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LoggingCog(bot))
