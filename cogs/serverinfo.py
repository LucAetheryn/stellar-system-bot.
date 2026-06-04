"""
Stellar System V2 — Server Info Cog
Commands: /serverinfo, /userinfo, /avatar, /roleinfo
"""

from __future__ import annotations

from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from utils.config import BOT_COLOR
from utils.logger import log


class ServerInfoCog(commands.Cog, name="Server Info"):
    """Server and user information commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ── /serverinfo ───────────────────────────────────────────────────────────

    @app_commands.command(name="serverinfo", description="Display detailed information about this server.")
    async def serverinfo(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if not guild:
            return

        await guild.chunk()  # Ensure member cache is populated

        embed = discord.Embed(
            title=f"🏠  {guild.name}",
            color=BOT_COLOR,
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(name="Owner", value=f"<@{guild.owner_id}>", inline=True)
        embed.add_field(name="Members", value=f"{guild.member_count:,}", inline=True)
        embed.add_field(name="Boosts", value=f"{guild.premium_subscription_count} (Tier {guild.premium_tier})", inline=True)
        embed.add_field(name="Channels", value=f"{len(guild.channels)}", inline=True)
        embed.add_field(name="Roles", value=f"{len(guild.roles)}", inline=True)
        embed.add_field(name="Emojis", value=f"{len(guild.emojis)}", inline=True)
        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(guild.created_at, style="D"),
            inline=True,
        )
        embed.add_field(
            name="Verification Level",
            value=str(guild.verification_level).replace("_", " ").title(),
            inline=True,
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.set_footer(text=f"Guild ID: {guild.id}")

        await interaction.response.send_message(embed=embed)
        log.info("Server info requested by %s in guild %d", interaction.user, guild.id)

    # ── /userinfo ─────────────────────────────────────────────────────────────

    @app_commands.command(name="userinfo", description="Display information about a user.")
    @app_commands.describe(member="The member to look up (defaults to you).")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None,
    ) -> None:
        target = member or interaction.user
        if not isinstance(target, discord.Member):
            await interaction.response.send_message("Could not find that member.", ephemeral=True)
            return

        roles = [r.mention for r in reversed(target.roles) if r.name != "@everyone"]

        embed = discord.Embed(
            title=f"👤  {target.display_name}",
            color=target.accent_color or BOT_COLOR,
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(name="Username", value=str(target), inline=True)
        embed.add_field(name="User ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Bot?", value="Yes" if target.bot else "No", inline=True)
        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(target.created_at, style="D"),
            inline=True,
        )
        embed.add_field(
            name="Joined Server",
            value=discord.utils.format_dt(target.joined_at, style="D") if target.joined_at else "Unknown",
            inline=True,
        )
        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=" ".join(roles[:10]) + ("…" if len(roles) > 10 else "") if roles else "None",
            inline=False,
        )

        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user}")

        await interaction.response.send_message(embed=embed)

    # ── /avatar ───────────────────────────────────────────────────────────────

    @app_commands.command(name="avatar", description="Display a user's avatar in full size.")
    @app_commands.describe(member="The member whose avatar to show (defaults to you).")
    async def avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None,
    ) -> None:
        target = member or interaction.user

        embed = discord.Embed(
            title=f"🖼️  {target.display_name}'s Avatar",
            color=BOT_COLOR,
        )

        avatar_url = target.display_avatar.url
        embed.set_image(url=avatar_url)
        embed.add_field(
            name="Download",
            value=f"[PNG]({target.display_avatar.replace(format='png', size=1024).url}) | "
                  f"[JPG]({target.display_avatar.replace(format='jpg', size=1024).url}) | "
                  f"[WEBP]({target.display_avatar.replace(format='webp', size=1024).url})",
        )

        await interaction.response.send_message(embed=embed)

    # ── /roleinfo ─────────────────────────────────────────────────────────────

    @app_commands.command(name="roleinfo", description="Display information about a role.")
    @app_commands.describe(role="The role to inspect.")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role) -> None:
        members_with_role = len(role.members)

        embed = discord.Embed(
            title=f"🏷️  {role.name}",
            color=role.color,
            timestamp=datetime.now(timezone.utc),
        )

        embed.add_field(name="Role ID", value=f"`{role.id}`", inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Members", value=str(members_with_role), inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Managed", value="Yes" if role.managed else "No", inline=True)
        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(role.created_at, style="D"),
            inline=True,
        )
        embed.add_field(name="Position", value=str(role.position), inline=True)

        key_perms = [
            perm.replace("_", " ").title()
            for perm, value in iter(role.permissions)
            if value and perm in {
                "administrator", "manage_guild", "manage_roles", "manage_channels",
                "kick_members", "ban_members", "manage_messages", "mention_everyone",
            }
        ]
        embed.add_field(
            name="Key Permissions",
            value=", ".join(key_perms) if key_perms else "None",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerInfoCog(bot))
