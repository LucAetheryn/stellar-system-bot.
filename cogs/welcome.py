import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(799075847801143327)

        if channel:
            member_count = len(member.guild.members)

            welcome_msg = (
                f"Welcome {member.mention} ke **Stellar Universe**!\n"
                f"Kamu member ke **#{member_count}**"
            )

            await channel.send(welcome_msg)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
