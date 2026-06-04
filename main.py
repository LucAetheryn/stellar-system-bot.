import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents
)

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Game(name="Managing Stellar System")
    )

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

    print(f"{bot.user} is online!")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Failed loading {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
