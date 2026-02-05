import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Managing Stellar System"))
    print(f'{bot.user} is online!')

@bot.command()
async def owner(ctx):
    embed = discord.Embed(
        title="<:StellarUniverse:1468863371427450890> About Owner",
        color=0xBB86FC # Warna ungu senada logo
    )
    
    # Menggunakan inline=True agar link media sosial berjejer ke samping
    embed.add_field(name="<a:Instagram:1468872411599339530> Instagram", value="<a:Arrow:820637327969746974> [Lucky.praditya](https://www.instagram.com/Lucky.praditya/)", inline=True)
    embed.add_field(name="<a:Twitter:820587292363718656> Twitter", value="<a:Arrow:820637327969746974> [luckypraditya1](https://twitter.com/luckypraditya1?s=09)", inline=True)
    embed.add_field(name="<a:YouTube:1468872494705410079> YouTube", value="<a:Arrow:820637327969746974> [Channel](https://youtube.com/channel/UCcHVBAX0fSBOctB_tKPDk5Q)", inline=True)
    embed.add_field(name="<a:Discord:820576752576888902> Discord", value="<a:Arrow:820637327969746974> [Stellar Universe](https://discord.gg/QEhHc6UBHH)", inline=True)
    embed.add_field(name="<a:Spotify:1468872357165793324> Spotify", value="<a:Arrow:820637327969746974> [Lucky Praditya](https://open.spotify.com/user/nr1804ww5fuzdnmh4o3nkce06?si=AvEXNb3aRUKAla_hELGXsA)", inline=True)
    embed.add_field(name="<a:Tiktok:1468877397033222164> Tiktok", value="<a:Arrow:820637327969746974> [luc.aetheryn](https://www.tiktok.com/@luc.aetheryn)", inline=True)
    
    
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def rules(ctx):
    # Teks rules murni sesuai permintaan tanpa perubahan teks sama sekali
    rules_message = (
        "<a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847><a:1_:853534476344098847>\n"
        "                           <a:___:859993289113731123>     ***RULES*** <a:___:859993289113731123> \n"
        "<a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265><a:2_:853534457457803265>\n\n"
        "**Kami memiliki aturan untuk mengakomodasi komunitas kami**\n\n"
        "**1. Harap menghormati semua orang**\n Anda bebas untuk mengungkapkan pendapat yang berbeda tetapi juga menghormati orang lain.\n\n"
        "**2. Hindari perilaku buruk**\n Bersikaplah sopan. Itu saja. Argumen politik / agama juga boleh-boleh saja - tetapi bukan untuk merendahkan orang lain.\n\n"
        "**3. Jangan Spam**\n Jangan melakukan spam, seperti teks, gambar, emoji, reaksi emoji, audio yang mengganggu. Anda akan Dipenjara dan spam yang berkelanjutan akan di ban dari server.\n\n"
        "**4. Jangan Beriklan**\n Jangan mempromosikan sendiri server Anda atau server lain tanpa izin. termasuk memposting tautan undangan, baik sosial media atau pun link penjualan ilegal.\n\n"
        "**5. Hindari drama & Jangan Sirkel2an**\n Cobalah untuk tidak memulai drama yang tidak perlukan. Lapor admin / staff bila ada yang membuat kegaduhan\n\n"
        "**6. Gunakan channel sesuai namanya**\n Kami memiliki channel yang berbeda untuk tema bahasan diserver, jadi misalkan jika ingin mabar bisa ke mabar dan sesuai channel masing-masing.\n\n"
        "**7. Dilarang menggunakan nickname toxic / foto profile yang dapat menimbulkan permasalahan**\n Mohon menggunakan nick name dan profile picture SFW alias aman untuk semua umur tanpa mengandung unsur SARA atau mengundang pertikaian."
    )
    
    embed = discord.Embed(
        description=rules_message,
        color=0xBB86FC
    )
    await ctx.send(embed=embed)

token = os.getenv('TOKEN')
bot.run(token)
