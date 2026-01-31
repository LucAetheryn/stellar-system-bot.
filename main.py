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
        title="🚀 About Owner",
        description=(
            "<a:Instagram:820584675008577546> ***Instagram*** <a:Arrow:820637327969746974> [Lucky.praditya](https://www.instagram.com/Lucky.praditya/)\n"
            "<a:Twitter:820587292363718656> ***Twitter*** <a:Arrow:820637327969746974> [luckypraditya1](https://twitter.com/luckypraditya1?s=09)\n"
            "<a:YouTube:820587271199653918> ***YouTube*** <a:Arrow:820637327969746974> [Channel YouTube](https://youtube.com/channel/UCcHVBAX0fSBOctB_tKPDk5Q)\n"
            "<a:Discord:820576752576888902> ***Discord*** <a:Arrow:820637327969746974> [Stellar Universe](https://discord.gg/QEhHc6UBHH)"
        ),
        color=0xBB86FC  # Warna ungu senada logo
    )
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def rules(ctx):
    # Header dekorasi menggunakan emoji yang kamu berikan
    header = "<a:1_:853534476344098847>" * 10
    
    embed = discord.Embed(
        title=f"{header}\nRULES STELLAR UNIVERSE\n{header}",
        description="**Kami memiliki aturan untuk mengakomodasi komunitas kami**",
        color=0xBB86FC
    )
    
    embed.add_field(name="1. Harap menghormati semua orang", value="Anda bebas untuk mengungkapkan pendapat yang berbeda tetapi juga menghormati orang lain.", inline=False)
    embed.add_field(name="2. Hindari perilaku buruk", value="Bersikaplah sopan. Argumen politik/agama boleh saja, tapi bukan untuk merendahkan.", inline=False)
    embed.add_field(name="3. Jangan Spam", value="Teks, gambar, atau emoji berlebihan akan dipenjara/ban.", inline=False)
    embed.add_field(name="4. Jangan Beriklan", value="Dilarang promosi server lain/sosmed tanpa izin.", inline=False)
    embed.add_field(name="5. Hindari drama & Sirkel2an", value="Jangan mulai drama. Lapor staff jika ada kegaduhan.", inline=False)
    embed.add_field(name="6. Gunakan channel sesuai namanya", value="Gunakan channel sesuai tema bahasan masing-masing.", inline=False)
    embed.add_field(name="7. Nickname & Foto Profil SFW", value="Gunakan identitas yang aman (SFW) tanpa unsur SARA.", inline=False)
    
    embed.set_footer(text="Terima kasih telah mematuhi aturan Stellar Universe!")
    
    await ctx.send(embed=embed)

token = os.getenv('TOKEN')
bot.run(token)
