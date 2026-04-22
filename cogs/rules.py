import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self, ctx):

        rules_message = (
"<a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847>\n"
"                           <a::859993289113731123>     RULES <a::859993289113731123> \n"
"<a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265>\n\n"
"Kami memiliki aturan untuk mengakomodasi komunitas kami\n\n"
"1. Harap menghormati semua orang\n Anda bebas untuk mengungkapkan pendapat yang berbeda tetapi juga menghormati orang lain.\n\n"
"2. Hindari perilaku buruk\n Bersikaplah sopan. Itu saja. Argumen politik / agama juga boleh-boleh saja - tetapi bukan untuk merendahkan orang lain.\n\n"
"3. Jangan Spam\n Jangan melakukan spam, seperti teks, gambar, emoji, reaksi emoji, audio yang mengganggu. Anda akan Dipenjara dan spam yang berkelanjutan akan di ban dari server.\n\n"
"4. Jangan Beriklan\n Jangan mempromosikan sendiri server Anda atau server lain tanpa izin. termasuk memposting tautan undangan, baik sosial media atau pun link penjualan ilegal.\n\n"
"5. Hindari drama & Jangan Sirkel2an\n Cobalah untuk tidak memulai drama yang tidak perlukan. Lapor admin / staff bila ada yang membuat kegaduhan\n\n"
"6. Gunakan channel sesuai namanya\n Kami memiliki channel yang berbeda untuk tema bahasan diserver, jadi misalkan jika ingin mabar bisa ke mabar dan sesuai channel masing-masing.\n\n"
"7. Dilarang menggunakan nickname toxic / foto profile yang dapat menimbulkan permasalahan\n Mohon menggunakan nick name dan profile picture SFW alias aman untuk semua umur tanpa mengandung unsur SARA atau mengundang pertikaian."
)

        embed = discord.Embed(
            description=rules_message,
            color=0xBB86FC
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))
