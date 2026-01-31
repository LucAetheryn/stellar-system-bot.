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
    await ctx.send("🚀 **About Owner**:\nOwner dari Stellar Universe adalah **MaxmunZ**. Membangun ekosistem bintang untuk semua!")

@bot.command()
async def rules(ctx):
    rules_text = (
        "📜 **Stellar Rules**:\n"
        "1. Hormati sesama penghuni bintang.\n"
        "2. Dilarang spam atau mengirim link berbahaya.\n"
        "3. Ikuti instruksi Moderator."
    )
    await ctx.send(rules_text)

token = os.getenv('TOKEN')
bot.run(token)
