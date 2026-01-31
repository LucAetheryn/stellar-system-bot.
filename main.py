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
        description="Hubungi owner Stellar Universe melalui platform di bawah ini:",
        color=0xBB86FC
    )
    # Link dibuat sejajar menggunakan inline=True
    embed.add_field(name="📸 Instagram", value="[Lucky.praditya](https://www.instagram.com/Lucky.praditya/)", inline=True)
    embed.add_field(name="🐦 Twitter", value="[luckypraditya1](https://twitter.com/luckypraditya1?s=09)", inline=True)
    embed.add_field(name="🎥 YouTube", value="[Channel](https://youtube.com/channel/UCcHVBAX0fSBOctB_tKPDk5Q)", inline=True)
    embed.add_field(name="💬 Discord", value="[Stellar Universe](https://discord.gg/QEhHc6UBHH)", inline=True)
    
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def rules(ctx):
    header = "✨ " + "━" * 10 + " ✨"
    embed = discord.Embed(
        title=f"{header}\nRULES STELLAR UNIVERSE\n{header}",
        description="**Harap patuhi aturan demi kenyamanan bersama**",
        color=0xBB86FC
    )
    
    rules_list = [
        ("1. Hormati Sesama", "Hargai pendapat orang lain dan bersikap sopan."),
        ("2. No Bad Behavior", "Hindari politik/sara yang merendahkan."),
        ("3. No Spam", "Dilarang spam teks, gambar, atau emoji berlebihan."),
        ("4. No Advertising", "Dilarang promosi tanpa izin admin."),
        ("5. Hindari Drama", "Jangan memancing keributan atau sirkel-sirkelan."),
        ("6. Sesuai Channel", "Gunakan channel sesuai dengan fungsinya."),
        ("7. SFW Profile", "Gunakan nama dan foto profil yang aman/sopan.")
    ]
    
    for name, value in rules_list:
        embed.add_field(name=name, value=value, inline=False)
        
    embed.set_footer(text="Stellar System | Melayani dengan Bintang")
    await ctx.send(embed=embed)

token = os.getenv('TOKEN')
bot.run(token)
