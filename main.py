import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN environment variable not found!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Logged in as : {bot.user}")
    print(f"Bot ID       : {bot.user.id}")
    print(f"Guilds       : {len(bot.guilds)}")
    print("=" * 50)

    await bot.change_presence(
        activity=discord.Game(name="Managing Stellar System")
    )

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")

        for command in synced:
            print(f"   ↳ /{command.name}")

    except Exception as e:
        print(f"❌ Failed to sync commands:")
        print(e)

    print("✅ Bot is fully online")


@bot.event
async def on_command_error(ctx, error):
    print(f"❌ Command Error: {error}")


async def load_extensions():
    print("Loading cogs...")

    if not os.path.exists("./cogs"):
        print("❌ cogs folder not found!")
        return

    loaded = 0

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"

            try:
                await bot.load_extension(cog_name)
                loaded += 1
                print(f"✅ Loaded {cog_name}")

            except Exception as e:
                print(f"❌ Failed loading {cog_name}")
                print(f"   Error: {e}")

    print(f"Loaded {loaded} cog(s)")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
