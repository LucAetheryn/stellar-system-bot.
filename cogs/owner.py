import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self, ctx):
        embed = discord.Embed(
            title="Server Rules",
            description="Kami memiliki aturan untuk mengakomodasi komunitas kami",
            color=0xBB86FC
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))
