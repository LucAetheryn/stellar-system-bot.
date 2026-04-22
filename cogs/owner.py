import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def owner(self, ctx):
        embed = discord.Embed(
            title="<:StellarUniverse:1468863371427450890> About Owner",
            color=0xBB86FC
        )

        embed.add_field(name="Instagram", value="[Lucky.praditya](https://www.instagram.com/Lucky.praditya/)", inline=True)
        embed.add_field(name="Twitter", value="[luckypraditya1](https://twitter.com)", inline=True)
        embed.add_field(name="YouTube", value="Channel", inline=True)

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Owner(bot))
