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
                f"<a:2_:853534457457803265> <a:1_:853534476344098847> <a:2_:853534457457803265> <a:1_:853534476344098847> <a:2_:853534457457803265>\n\n"
                f"[<a:Pika:853530949357797396>] Welcome To **Stellar Universe**\n\n"
                f"<a:MZ:853520576240680960>〢User Registed {member.mention}\n"
                f"<a:MZ:853520576240680960>〢User Position **#{member_count}**\n"
                f"<a:MZ:853520576240680960>〢Server Name **Stellar Universe**"
            )

            await channel.send(welcome_msg)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
