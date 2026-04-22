import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self, ctx):
        embed = discord.Embed(
            title="Server Rules",
            description=""<a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847>\n"
        "                           <a:___:859993289113731123>     ***RULES*** <a:___:859993289113731123> \n"
        "<a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265>\n\n"
        "**Kami memiliki aturan untuk mengakomodasi komunitas kami**\n\n"
        "**1. Harap menghormati semua orang**\n Anda bebas untuk mengungkapkan pendapat yang berbeda tetapi juga menghormati orang lain.\n\n"
        "**2. Hindari perilaku buruk**\n Bersikaplah sopan.\n\n"
        "**3. Jangan Spam**\n Jangan melakukan spam.\n\n"
        "**4. Jangan Beriklan**\n Jangan mempromosikan sendiri server Anda.\n\n"
        "**5. Hindari drama & Jangan Sirkel2an**\n Cobalah untuk tidak memulai drama.\n\n"
        "**6. Gunakan channel sesuai namanya**\n Gunakan channel sesuai.\n\n"
        "**7. Dilarang nickname toxic**"",
            color=0xBB86FC
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))
