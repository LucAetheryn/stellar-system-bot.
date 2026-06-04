"""
Stellar System V2 — Utility Cog
Commands: /ping, /uptime, /botinfo, /help
"""

from __future__ import annotations

from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from utils.config import BOT_COLOR, BOT_NAME, BOT_VERSION
from utils.logger import log

# Bot start time recorded at import time
_START_TIME: datetime = datetime.now(timezone.utc)


class UtilityCog(commands.Cog, name="Utility"):
    """General utility and information commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── /ping ─────────────────────────────────────────────────────────────────

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)

        color = (
            0x57F287 if latency_ms < 100
            else 0xFEE75C if latency_ms < 200
            else 0xFF5555
        )

        embed = discord.Embed(
            title="🏓  Pong!",
            color=color,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="WebSocket Latency", value=f"`{latency_ms} ms`", inline=True)
        await interaction.response.send_message(embed=embed)

    # ── /uptime ───────────────────────────────────────────────────────────────

    @app_commands.command(name="uptime", description="Show how long the bot has been running.")
    async def uptime(self, interaction: discord.Interaction) -> None:
        now = datetime.now(timezone.utc)
        delta = now - _START_TIME

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = (
            f"{days}d {hours}h {minutes}m {seconds}s"
            if days
            else f"{hours}h {minutes}m {seconds}s"
            if hours
            else f"{minutes}m {seconds}s"
        )

        embed = discord.Embed(
            title="⏱️  Uptime",
            description=f"The bot has been online for **{uptime_str}**.",
            color=BOT_COLOR,
            timestamp=now,
        )
        embed.add_field(
            name="Online Since",
            value=discord.utils.format_dt(_START_TIME, style="F"),
        )

        await interaction.response.send_message(embed=embed)

    # ── /botinfo ──────────────────────────────────────────────────────────────

    @app_commands.command(name="botinfo", description="Display information about this bot.")
    async def botinfo(self, interaction: discord.Interaction) -> None:
        bot = self.bot
        guild_count = len(bot.guilds)
        member_count = sum(g.member_count or 0 for g in bot.guilds)
        latency_ms = round(bot.latency * 1000)

        embed = discord.Embed(
            title=f"🤖  {BOT_NAME}",
            description="A professional, feature-rich Discord bot for the Stellar Universe server.",
            color=BOT_COLOR,
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(name="Version", value=f"`{BOT_VERSION}`", inline=True)
        embed.add_field(name="Servers", value=f"{guild_count:,}", inline=True)
        embed.add_field(name="Members", value=f"{member_count:,}", inline=True)
        embed.add_field(name="Latency", value=f"`{latency_ms} ms`", inline=True)
        embed.add_field(name="Library", value=f"discord.py `{discord.__version__}`", inline=True)
        embed.add_field(name="Commands", value=f"{len(bot.tree.get_commands()):,} slash commands", inline=True)

        if bot.user and bot.user.avatar:
            embed.set_thumbnail(url=bot.user.avatar.url)

        embed.set_footer(text="Stellar Universe • Made with ♥")
        await interaction.response.send_message(embed=embed)

    # ── /help ─────────────────────────────────────────────────────────────────

    @app_commands.command(name="help", description="Display all available commands by category.")
    async def help_cmd(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="📖  Stellar System V2 — Command Help",
            description="All available slash commands organised by category.",
            color=BOT_COLOR,
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(
            name="ℹ️  Information",
            value=(
                "`/serverinfo` — Server details\n"
                "`/userinfo` — User profile\n"
                "`/avatar` — Full-size avatar\n"
                "`/roleinfo` — Role details\n"
                "`/owner` — Bot owner links\n"
                "`/rules` — Server rules"
            ),
            inline=True,
        )

        embed.add_field(
            name="🔨  Moderation",
            value=(
                "`/kick` — Kick a member\n"
                "`/ban` — Ban a member\n"
                "`/unban` — Unban a user by ID\n"
                "`/timeout` — Timeout a member\n"
                "`/untimeout` — Remove timeout\n"
                "`/purge` — Bulk delete messages\n"
                "`/warn` — Issue a warning\n"
                "`/warnings` — View warnings\n"
                "`/removewarn` — Delete a warning"
            ),
            inline=True,
        )

        embed.add_field(
            name="🎫  Tickets",
            value=(
                "`/ticketpanel` — Post ticket panel *(Admin)*\n"
                "`/close` — Close this ticket\n"
                "`/transcript` — Save chat history\n"
                "`/delete` — Delete ticket channel"
            ),
            inline=True,
        )

        embed.add_field(
            name="⚙️  Admin",
            value=(
                "`/setwelcome` — Set welcome channel\n"
                "`/setlog` — Set log channel\n"
                "`/viewlog` — View log channel\n"
                "`/setautorole` — Add auto-role\n"
                "`/remautorole` — Remove auto-role\n"
                "`/viewautorole` — View auto-roles"
            ),
            inline=True,
        )

        embed.add_field(
            name="🛠️  Utility",
            value=(
                "`/ping` — Check latency\n"
                "`/uptime` — Bot online duration\n"
                "`/botinfo` — Bot statistics\n"
                "`/help` — This menu"
            ),
            inline=True,
        )

        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(text="Stellar Universe • Use / to trigger commands")
        await interaction.response.send_message(embed=embed)
        log.info("Help command invoked by %s", interaction.user)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UtilityCog(bot))
