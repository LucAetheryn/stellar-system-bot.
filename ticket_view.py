"""
Stellar System V2 — Ticket Views
Persistent UI components for the ticket panel.
The view is added as a persistent view so it survives bot restarts.
"""

from __future__ import annotations

import discord

import database as db
from utils import embeds
from utils.config import STAFF_ROLE_ID
from utils.logger import log


class TicketPanelView(discord.ui.View):
    """View attached to the ticket panel message — contains the Create Ticket button."""

    def __init__(self) -> None:
        super().__init__(timeout=None)  # persistent

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.primary,
        emoji="🎫",
        custom_id="ticket:create",
    )
    async def create_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        guild = interaction.guild
        user = interaction.user

        if guild is None:
            return

        # --- Prevent duplicate open tickets ---
        existing = await db.get_open_ticket(guild.id, user.id)  # type: ignore[union-attr]
        if existing:
            channel = guild.get_channel(existing["channel_id"])
            mention = channel.mention if channel else "an existing channel"
            await interaction.response.send_message(
                embed=embeds.warning(
                    "Ticket Already Open",
                    f"You already have an open ticket: {mention}",
                ),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        # --- Build permission overwrites ---
        overwrites: dict[discord.abc.Snowflake, discord.PermissionOverwrite] = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(  # type: ignore[dict-item]
                view_channel=True,
                send_messages=True,
                attach_files=True,
                embed_links=True,
            ),
        }

        # Grant staff role access if configured
        if STAFF_ROLE_ID:
            staff_role = guild.get_role(STAFF_ROLE_ID)
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_messages=True,
                )

        # Grant bot itself access
        if guild.me:
            overwrites[guild.me] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                manage_messages=True,
            )

        # --- Create the ticket channel ---
        try:
            channel = await guild.create_text_channel(
                name=f"ticket-{user.name}",
                overwrites=overwrites,
                reason=f"Ticket opened by {user}",
            )
        except discord.Forbidden:
            await interaction.followup.send(
                embed=embeds.error("Permission Error", "I don't have permission to create channels."),
                ephemeral=True,
            )
            return
        except discord.HTTPException as exc:
            log.error("Failed to create ticket channel: %s", exc)
            await interaction.followup.send(
                embed=embeds.error("Error", "Failed to create your ticket channel."),
                ephemeral=True,
            )
            return

        ticket_id = await db.create_ticket(guild.id, channel.id, user.id)  # type: ignore[union-attr]

        # --- Send intro message inside ticket ---
        intro_embed = discord.Embed(
            title="🎫  Support Ticket",
            description=(
                f"Welcome {user.mention}!\n\n"
                "Please describe your issue and a staff member will assist you shortly.\n\n"
                "To close this ticket use `/close`."
            ),
            color=0xBB86FC,
        )
        intro_embed.set_footer(text=f"Ticket #{ticket_id}")

        await channel.send(
            content=user.mention,
            embed=intro_embed,
            view=TicketActionView(),
        )

        log.info("Ticket #%d created by %s (%d) in guild %d", ticket_id, user, user.id, guild.id)

        await interaction.followup.send(
            embed=embeds.success("Ticket Created", f"Your ticket has been created: {channel.mention}"),
            ephemeral=True,
        )


class TicketActionView(discord.ui.View):
    """Buttons shown inside an open ticket channel."""

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="ticket:close_btn",
    )
    async def close_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            return

        ticket = await db.get_ticket_by_channel(channel.id)
        if not ticket or ticket["status"] != "open":
            await interaction.response.send_message(
                embed=embeds.error("Not a Ticket", "This channel is not an active ticket."),
                ephemeral=True,
            )
            return

        await db.close_ticket(channel.id)

        embed = embeds.info(
            "Ticket Closed",
            f"This ticket was closed by {interaction.user.mention}.",
        )
        await interaction.response.send_message(embed=embed)

        # Lock the channel for the ticket owner
        try:
            ticket_owner = interaction.guild.get_member(ticket["user_id"]) if interaction.guild else None
            if ticket_owner:
                await channel.set_permissions(ticket_owner, send_messages=False)
        except discord.Forbidden:
            pass

        log.info("Ticket channel %d closed by %s", channel.id, interaction.user)
