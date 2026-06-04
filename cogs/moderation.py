"""
Stellar System V2 — Moderation Cog
Full suite of moderation slash commands with warning persistence.
All actions are logged to the configured log channel.
"""

from __future__ import annotations

import traceback
from datetime import datetime, timedelta, timezone

import discord
from discord import app_commands
from discord.ext import commands

from database import database as db
from utils import embeds
from utils.checks import is_moderator
from utils.logger import log


class ModerationCog(commands.Cog, name="Moderation"):
    """Moderation commands — kick, ban, timeout, purge, and warnings."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── Internal: log moderation action ──────────────────────────────────────

    async def _mod_log(
        self,
        guild: discord.Guild,
        action: str,
        moderator: discord.Member | discord.User,
        target: discord.Member | discord.User,
        reason: str,
        color: int = 0xFEE75C,
    ) -> None:
        """Send a moderation action embed to the configured log channel."""
        channel_id = await db.get_log_channel(guild.id)
        if not channel_id:
            return

        channel = guild.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        embed = discord.Embed(
            title=f"🔨  {action}",
            color=color,
            timestamp=datetime.now(timezone.utc),
        )
        embed.add_field(name="Target", value=f"{target.mention} (`{target.id}`)", inline=True)
        embed.add_field(name="Moderator", value=f"{moderator.mention} (`{moderator.id}`)", inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            log.warning("Cannot send mod log to channel %d", channel_id)

    # ── /kick ─────────────────────────────────────────────────────────────────

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.describe(member="The member to kick.", reason="Reason for the kick.")
    @is_moderator()
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided.",
    ) -> None:
        if member.top_role >= interaction.user.top_role:  # type: ignore[union-attr]
            await interaction.response.send_message(
                embed=embeds.error("Hierarchy Error", "You cannot kick someone with an equal or higher role."),
                ephemeral=True,
            )
            return

        try:
            await member.kick(reason=f"{interaction.user}: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=embeds.error("Permission Error", "I cannot kick that member."),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=embeds.success("Member Kicked", f"{member.mention} has been kicked.\n**Reason:** {reason}")
        )
        await self._mod_log(interaction.guild, "Kick", interaction.user, member, reason, 0xFEE75C)  # type: ignore[arg-type]
        log.info("Kicked %s from guild %d. Reason: %s", member, interaction.guild_id, reason)

    # ── /ban ──────────────────────────────────────────────────────────────────

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.describe(member="The member to ban.", reason="Reason for the ban.", delete_days="Days of messages to delete (0-7).")
    @is_moderator()
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided.",
        delete_days: app_commands.Range[int, 0, 7] = 0,
    ) -> None:
        if member.top_role >= interaction.user.top_role:  # type: ignore[union-attr]
            await interaction.response.send_message(
                embed=embeds.error("Hierarchy Error", "You cannot ban someone with an equal or higher role."),
                ephemeral=True,
            )
            return

        try:
            await member.ban(reason=f"{interaction.user}: {reason}", delete_message_days=delete_days)
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=embeds.error("Permission Error", "I cannot ban that member."),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=embeds.success("Member Banned", f"{member.mention} has been banned.\n**Reason:** {reason}")
        )
        await self._mod_log(interaction.guild, "Ban", interaction.user, member, reason, 0xFF5555)  # type: ignore[arg-type]
        log.info("Banned %s from guild %d. Reason: %s", member, interaction.guild_id, reason)

    # ── /unban ────────────────────────────────────────────────────────────────

    @app_commands.command(name="unban", description="Unban a user by their user ID.")
    @app_commands.describe(user_id="The Discord user ID to unban.", reason="Reason for the unban.")
    @is_moderator()
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str = "No reason provided.",
    ) -> None:
        try:
            uid = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                embed=embeds.error("Invalid ID", "Please provide a valid numeric user ID."),
                ephemeral=True,
            )
            return

        guild = interaction.guild
        if guild is None:
            return

        try:
            ban_entry = await guild.fetch_ban(discord.Object(id=uid))
        except discord.NotFound:
            await interaction.response.send_message(
                embed=embeds.error("Not Banned", f"User `{uid}` is not banned on this server."),
                ephemeral=True,
            )
            return

        await guild.unban(ban_entry.user, reason=f"{interaction.user}: {reason}")

        await interaction.response.send_message(
            embed=embeds.success(
                "User Unbanned",
                f"**{ban_entry.user}** has been unbanned.\n**Reason:** {reason}",
            )
        )
        await self._mod_log(guild, "Unban", interaction.user, ban_entry.user, reason, 0x57F287)
        log.info("Unbanned user %d from guild %d. Reason: %s", uid, guild.id, reason)

    # ── /timeout ──────────────────────────────────────────────────────────────

    @app_commands.command(name="timeout", description="Timeout (mute) a member for a specified duration.")
    @app_commands.describe(
        member="The member to timeout.",
        minutes="Duration in minutes (1–40320 / 28 days).",
        reason="Reason for the timeout.",
    )
    @is_moderator()
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str = "No reason provided.",
    ) -> None:
        until = discord.utils.utcnow() + timedelta(minutes=minutes)
        try:
            await member.timeout(until, reason=f"{interaction.user}: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=embeds.error("Permission Error", "I cannot timeout that member."),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=embeds.success(
                "Member Timed Out",
                f"{member.mention} has been timed out for **{minutes} minute(s)**.\n**Reason:** {reason}",
            )
        )
        await self._mod_log(interaction.guild, "Timeout", interaction.user, member, f"{reason} ({minutes}m)", 0xFEE75C)  # type: ignore[arg-type]
        log.info("Timed out %s for %d minutes in guild %d.", member, minutes, interaction.guild_id)

    # ── /untimeout ────────────────────────────────────────────────────────────

    @app_commands.command(name="untimeout", description="Remove an active timeout from a member.")
    @app_commands.describe(member="The member whose timeout to remove.", reason="Reason for removal.")
    @is_moderator()
    async def untimeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided.",
    ) -> None:
        try:
            await member.timeout(None, reason=f"{interaction.user}: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=embeds.error("Permission Error", "I cannot remove the timeout from that member."),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=embeds.success("Timeout Removed", f"{member.mention}'s timeout has been removed.")
        )
        await self._mod_log(interaction.guild, "Untimeout", interaction.user, member, reason, 0x57F287)  # type: ignore[arg-type]
        log.info("Removed timeout from %s in guild %d.", member, interaction.guild_id)

    # ── /purge ────────────────────────────────────────────────────────────────

    @app_commands.command(name="purge", description="Bulk-delete messages from this channel.")
    @app_commands.describe(amount="Number of messages to delete (1–100).")
    @is_moderator()
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100],
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                embed=embeds.error("Error", "This command can only be used in text channels."),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await channel.purge(limit=amount)
        except discord.Forbidden:
            await interaction.followup.send(
                embed=embeds.error("Permission Error", "I don't have permission to delete messages here."),
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            embed=embeds.success("Messages Purged", f"Deleted **{len(deleted)}** message(s)."),
            ephemeral=True,
        )
        log.info("Purged %d messages in channel %d by %s.", len(deleted), channel.id, interaction.user)

    # ── /warn ─────────────────────────────────────────────────────────────────

    @app_commands.command(name="warn", description="Issue a warning to a member.")
    @app_commands.describe(member="The member to warn.", reason="Reason for the warning.")
    @is_moderator()
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str,
    ) -> None:
        warn_id = await db.add_warning(
            interaction.guild_id,  # type: ignore[arg-type]
            member.id,
            interaction.user.id,
            reason,
        )

        await interaction.response.send_message(
            embed=embeds.warning(
                "Warning Issued",
                f"{member.mention} has received warning `#{warn_id}`.\n**Reason:** {reason}",
            )
        )

        # DM the warned user
        try:
            await member.send(
                embed=embeds.warning(
                    "You Have Been Warned",
                    f"You received a warning in **{interaction.guild.name}**.\n**Reason:** {reason}",  # type: ignore[union-attr]
                )
            )
        except discord.Forbidden:
            pass

        await self._mod_log(interaction.guild, "Warning", interaction.user, member, reason, 0xFEE75C)  # type: ignore[arg-type]
        log.info("Warned %s (warn #%d) in guild %d. Reason: %s", member, warn_id, interaction.guild_id, reason)

    # ── /warnings ─────────────────────────────────────────────────────────────

    @app_commands.command(name="warnings", description="View all warnings for a member.")
    @app_commands.describe(member="The member whose warnings to view.")
    @is_moderator()
    async def warnings(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        warns = await db.get_warnings(interaction.guild_id, member.id)  # type: ignore[arg-type]

        if not warns:
            await interaction.response.send_message(
                embed=embeds.info("No Warnings", f"{member.mention} has no warnings."),
                ephemeral=True,
            )
            return

        embed = embeds.info(
            f"Warnings — {member.display_name}",
            f"{member.mention} has **{len(warns)}** warning(s).\n\u200b",
        )

        for w in warns[:10]:  # Cap at 10 fields per embed
            embed.add_field(
                name=f"Warn #{w['warn_id']} • {w['created_at'][:10]}",
                value=f"**Reason:** {w['reason']}\n**By:** <@{w['moderator_id']}>",
                inline=False,
            )

        if member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ── /removewarn ───────────────────────────────────────────────────────────

    @app_commands.command(name="removewarn", description="Remove a specific warning by its ID.")
    @app_commands.describe(warn_id="The warning ID to remove.")
    @is_moderator()
    async def removewarn(
        self, interaction: discord.Interaction, warn_id: int
    ) -> None:
        removed = await db.remove_warning(warn_id, interaction.guild_id)  # type: ignore[arg-type]

        if removed:
            await interaction.response.send_message(
                embed=embeds.success("Warning Removed", f"Warning `#{warn_id}` has been deleted."),
                ephemeral=True,
            )
            log.info("Removed warn #%d in guild %d by %s.", warn_id, interaction.guild_id, interaction.user)
        else:
            await interaction.response.send_message(
                embed=embeds.error("Not Found", f"Warning `#{warn_id}` does not exist in this server."),
                ephemeral=True,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModerationCog(bot))
