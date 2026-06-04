"""
Stellar System V2 — Auto Role Cog
Automatically assigns one or more roles when a new member joins.
Roles are persisted in SQLite and managed via slash commands.
"""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

import database as db
from utils import embeds
from utils.checks import is_admin
from utils.logger import log


class AutoRoleCog(commands.Cog, name="AutoRole"):
    """Auto-assign roles to new members."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── Event: member join ────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        role_ids = await db.get_autoroles(member.guild.id)
        if not role_ids:
            return

        roles_to_add: list[discord.Role] = []
        for role_id in role_ids:
            role = member.guild.get_role(role_id)
            if role:
                roles_to_add.append(role)

        if not roles_to_add:
            return

        try:
            await member.add_roles(*roles_to_add, reason="Auto-role on join")
            log.info(
                "Auto-roles %s assigned to %s (%d)",
                [r.name for r in roles_to_add],
                member,
                member.id,
            )
        except discord.Forbidden:
            log.warning("Cannot assign auto-roles to %s — missing Manage Roles permission.", member)
        except discord.HTTPException as exc:
            log.error("Failed to assign auto-roles to %s: %s", member, exc)

    # ── Slash command: /setautorole ───────────────────────────────────────────

    @app_commands.command(
        name="setautorole",
        description="Add a role to the auto-role list. (Admin only)",
    )
    @app_commands.describe(role="The role to automatically assign to new members.")
    @is_admin()
    async def setautorole(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> None:
        if role.is_bot_managed() or role.is_integration():
            await interaction.response.send_message(
                embed=embeds.error("Invalid Role", "Bot-managed or integration roles cannot be auto-assigned."),
                ephemeral=True,
            )
            return

        await db.add_autorole(interaction.guild_id, role.id)  # type: ignore[arg-type]
        await interaction.response.send_message(
            embed=embeds.success(
                "Auto-Role Added",
                f"{role.mention} will now be assigned to new members automatically.",
            )
        )
        log.info("Auto-role %s added in guild %d by %s", role.name, interaction.guild_id, interaction.user)

    # ── Slash command: /remautorole ───────────────────────────────────────────

    @app_commands.command(
        name="remautorole",
        description="Remove a role from the auto-role list. (Admin only)",
    )
    @app_commands.describe(role="The role to remove from the auto-role list.")
    @is_admin()
    async def remautorole(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> None:
        await db.remove_autorole(interaction.guild_id, role.id)  # type: ignore[arg-type]
        await interaction.response.send_message(
            embed=embeds.success(
                "Auto-Role Removed",
                f"{role.mention} has been removed from the auto-role list.",
            )
        )
        log.info("Auto-role %s removed in guild %d by %s", role.name, interaction.guild_id, interaction.user)

    # ── Slash command: /viewautorole ──────────────────────────────────────────

    @app_commands.command(
        name="viewautorole",
        description="View all currently configured auto-roles. (Admin only)",
    )
    @is_admin()
    async def viewautorole(self, interaction: discord.Interaction) -> None:
        role_ids = await db.get_autoroles(interaction.guild_id)  # type: ignore[arg-type]

        if not role_ids:
            await interaction.response.send_message(
                embed=embeds.info("Auto-Roles", "No auto-roles are currently configured."),
                ephemeral=True,
            )
            return

        guild = interaction.guild
        lines: list[str] = []
        for role_id in role_ids:
            role = guild.get_role(role_id) if guild else None  # type: ignore[union-attr]
            lines.append(role.mention if role else f"<Deleted Role: {role_id}>")

        embed = embeds.info(
            "Auto-Roles",
            "Roles automatically assigned when a new member joins:\n\n" + "\n".join(lines),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoRoleCog(bot))
