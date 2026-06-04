"""
Stellar System V2 — Role Selection View
Placeholder for future self-assignable role panels.
Can be extended with role-select menus for reaction-role-style features.
"""

from __future__ import annotations

import discord

from utils import embeds


class RoleSelectView(discord.ui.View):
    """
    Generic self-assignable role panel.
    Pass a list of (role_id, label, emoji) tuples to build the buttons.
    """

    def __init__(self, roles: list[tuple[int, str, str | None]]) -> None:
        super().__init__(timeout=None)
        for role_id, label, emoji in roles:
            self.add_item(_RoleButton(role_id=role_id, label=label, emoji=emoji))


class _RoleButton(discord.ui.Button):
    def __init__(self, role_id: int, label: str, emoji: str | None) -> None:
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=label,
            emoji=emoji,
            custom_id=f"role:{role_id}",
        )
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction) -> None:
        member = interaction.user
        guild = interaction.guild

        if not isinstance(member, discord.Member) or guild is None:
            return

        role = guild.get_role(self.role_id)
        if role is None:
            await interaction.response.send_message(
                embed=embeds.error("Role Not Found", "That role no longer exists."),
                ephemeral=True,
            )
            return

        if role in member.roles:
            await member.remove_roles(role, reason="Self-assignable role removed via panel")
            await interaction.response.send_message(
                embed=embeds.info("Role Removed", f"Removed **{role.name}** from your roles."),
                ephemeral=True,
            )
        else:
            await member.add_roles(role, reason="Self-assignable role added via panel")
            await interaction.response.send_message(
                embed=embeds.success("Role Added", f"Added **{role.name}** to your roles."),
                ephemeral=True,
            )
