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

        embed.add_field(name="<a:Instagram:1468872411599339530> Instagram", value="<a:Arrow:820637327969746974> [Lucky.praditya](https://www.instagram.com/Lucky.praditya/)", inline=True)
        embed.add_field(name="<a:Twitter:820587292363718656> Twitter", value="<a:Arrow:820637327969746974> [luckypraditya1](https://twitter.com/luckypraditya1?s=09)", inline=True)
        embed.add_field(name="<a:YouTube:1468872494705410079> YouTube", value="<a:Arrow:820637327969746974> [Channel](https://youtube.com/channel/UCcHVBAX0fSBOctB_tKPDk5Q)", inline=True)
        embed.add_field(name="<a:Discord:820576752576888902> Discord", value="<a:Arrow:820637327969746974> [Stellar Universe](https://discord.gg/QEhHc6UBHH)", inline=True)
        embed.add_field(name="<a:Spotify:1468872357165793324> Spotify", value="<a:Arrow:820637327969746974> [Lucky Praditya](https://open.spotify.com/user/nr1804ww5fuzdnmh4o3nkce06?si=AvEXNb3aRUKAla_hELGXsA)", inline=True)
        embed.add_field(name="<a:Tiktok:1468877397033222164> Tiktok", value="<a:Arrow:820637327969746974> [luc.aetheryn](https://www.tiktok.com/@luc.aetheryn)", inline=True)

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Owner(bot))
