"""
Stellar System V2 — Ticket Cog
Manages ticket lifecycle via slash commands.
The interactive panel is created by /ticketpanel.
"""

from __future__ import annotations

import io
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from database import database as db
from utils import embeds
from utils.checks import is_admin, is_moderator
from utils.logger import log
from views.ticket_view import TicketActionView, TicketPanelView


class TicketCog(commands.Cog, name="Tickets"):
    """Ticket system commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── Slash command: /ticketpanel ───────────────────────────────────────────

    @app_commands.command(
        name="ticketpanel",
        description="Send the ticket creation panel to this channel. (Admin only)",
    )
    @is_admin()
    async def ticketpanel(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="🎫  Support Tickets",
            description=(
                "Need help? Click the button below to open a private support ticket.\n\n"
                "A staff member will assist you as soon as possible.\n\n"
                "**Please do not abuse the ticket system.**"
            ),
            color=0xBB86FC,
        )
        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Stellar Universe • Support System")

        await interaction.response.send_message(
            embed=embeds.success("Panel Sent", "The ticket panel has been posted."),
            ephemeral=True,
        )
        await interaction.channel.send(embed=embed, view=TicketPanelView())  # type: ignore[union-attr]
        log.info("Ticket panel created in channel %d by %s", interaction.channel_id, interaction.user)

    # ── Slash command: /close ─────────────────────────────────────────────────

    @app_commands.command(name="close", description="Close the current ticket.")
    @is_moderator()
    async def close(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                embed=embeds.error("Error", "This command can only be used in a text channel."),
                ephemeral=True,
            )
            return

        ticket = await db.get_ticket_by_channel(channel.id)
        if not ticket or ticket["status"] != "open":
            await interaction.response.send_message(
                embed=embeds.error("Not a Ticket", "This channel is not an active ticket."),
                ephemeral=True,
            )
            return

        await db.close_ticket(channel.id)

        # Lock channel for the ticket owner
        guild = interaction.guild
        if guild:
            owner = guild.get_member(ticket["user_id"])
            if owner:
                try:
                    await channel.set_permissions(owner, send_messages=False)
                except discord.Forbidden:
                    pass

        await interaction.response.send_message(
            embed=embeds.info(
                "Ticket Closed",
                f"This ticket was closed by {interaction.user.mention}.\nUse `/delete` to remove the channel or `/transcript` to save the history.",
            )
        )
        log.info("Ticket channel %d closed by %s", channel.id, interaction.user)

    # ── Slash command: /transcript ────────────────────────────────────────────

    @app_commands.command(
        name="transcript",
        description="Save a transcript of the current ticket channel.",
    )
    @is_moderator()
    async def transcript(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                embed=embeds.error("Error", "Use this inside a ticket channel."),
                ephemeral=True,
            )
            return

        ticket = await db.get_ticket_by_channel(channel.id)
        if not ticket:
            await interaction.response.send_message(
                embed=embeds.error("Not a Ticket", "This channel is not a ticket."),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        lines: list[str] = [
            f"Stellar System V2 — Ticket Transcript",
            f"Channel: #{channel.name} ({channel.id})",
            f"Ticket ID: {ticket['ticket_id']}",
            f"Opened: {ticket['created_at']}",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC",
            "=" * 60,
            "",
        ]

        async for message in channel.history(limit=None, oldest_first=True):
            ts = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"[{ts}] {message.author} ({message.author.id}): {message.content}")
            for embed in message.embeds:
                if embed.title:
                    lines.append(f"  [EMBED] {embed.title}")
                if embed.description:
                    lines.append(f"  {embed.description}")

        content = "\n".join(lines)
        file = discord.File(
            fp=io.BytesIO(content.encode("utf-8")),
            filename=f"transcript-{channel.name}.txt",
        )

        await interaction.followup.send(
            embed=embeds.success("Transcript Ready", "The transcript has been attached below."),
            file=file,
            ephemeral=True,
        )
        log.info("Transcript generated for ticket channel %d by %s", channel.id, interaction.user)

    # ── Slash command: /delete ────────────────────────────────────────────────

    @app_commands.command(
        name="delete",
        description="Permanently delete the current ticket channel. (Moderator only)",
    )
    @is_moderator()
    async def delete(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                embed=embeds.error("Error", "Use this inside a ticket channel."),
                ephemeral=True,
            )
            return

        ticket = await db.get_ticket_by_channel(channel.id)
        if not ticket:
            await interaction.response.send_message(
                embed=embeds.error("Not a Ticket", "This channel is not a ticket."),
                ephemeral=True,
            )
            return

        await db.delete_ticket(channel.id)
        await interaction.response.send_message(
            embed=embeds.warning(
                "Deleting Ticket",
                "This channel will be deleted in 5 seconds.",
            )
        )

        import asyncio
        await asyncio.sleep(5)
        try:
            await channel.delete(reason=f"Ticket deleted by {interaction.user}")
        except discord.Forbidden:
            log.warning("Cannot delete ticket channel %d — missing permission.", channel.id)
        except discord.HTTPException as exc:
            log.error("Failed to delete ticket channel %d: %s", channel.id, exc)

        log.info("Ticket channel %d deleted by %s", channel.id, interaction.user)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicketCog(bot))
