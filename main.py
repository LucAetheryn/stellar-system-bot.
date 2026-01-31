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
    owner_text = (
        "<a:Instagram:820584675008577546> ***Instagram*** <a:Arrow:820637327969746974> https://www.instagram.com/Lucky.praditya/\n"
        "<a:Twitter:820587292363718656> ***Twitter*** <a:Arrow:820637327969746974> https://twitter.com/luckypraditya1?s=09\n"
        "<a:YouTube:820587271199653918> ***YouTube*** <a:Arrow:820637327969746974> https://youtube.com/channel/UCcHVBAX0fSBOctB_tKPDk5Q\n"
        "<a:Discord:820576752576888902> ***Discord*** <a:Arrow:820637327969746974> https://discord.gg/QEhHc6UBHH"
    )
    await ctx.send(owner_text)

@bot.command()
async def rules(ctx):
    rules_text = (
        "<a:1_:853534476344098847>" * 15 + "\n"
        "                           <a:___:859993289113731123>     ***RULES*** <a:___:859993289113731123>\n"
        "<a:2_:853534457457803265>" * 15 + "\n\n"
        "**Kami memiliki aturan untuk mengakomodasi komunitas kami**\n\n"
        "**1. Harap menghormati semua orang**\nAnda bebas untuk mengungkapkan pendapat yang berbeda tetapi juga menghormati orang lain.\n\n"
        "**2. Hindari perilaku buruk**\nBersikaplah sopan. Itu saja. Argumen politik / agama juga boleh-boleh saja - tetapi bukan untuk merendahkan orang lain.\n\n"
        "**3. Jangan Spam**\nJangan melakukan spam, seperti teks, gambar, emoji, reaksi emoji, audio yang mengganggu. Anda akan Dipenjara dan spam yang berkelanjutan akan di ban dari server.\n\n"
        "**4. Jangan Beriklan**\nJangan mempromosikan sendiri server Anda atau server lain tanpa izin. termasuk memposting tautan undangan, baik sosial media atau pun link penjualan ilegal.\n\n"
        "**5. Hindari drama & Jangan Sirkel2an**\nCobalah untuk tidak memulai drama yang tidak perlukan. Lapor admin / staff bila ada yang membuat kegaduhan\n\n"
        "**6. Gunakan channel sesuai namanya**\nKami memiliki channel yang berbeda untuk tema bahasan diserver, jadi misalkan jika ingin mabar bisa ke mabar dan sesuai channel masing-masing.\n\n"
        "**7. Dilarang menggunakan nickname toxic / foto profile yang dapat menimbulkan permasalahan**\nMohon menggunakan nick name dan profile picture SFW alias aman untuk semua umur tanpa mengandung unsur SARA atau mengundang pertikaian."
    )
    await ctx.send(rules_text)

token = os.getenv('TOKEN')
bot.run(token)
