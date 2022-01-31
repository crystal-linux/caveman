# Stdlib
import os
from datetime import datetime

# Pip
import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(";"),
    description="Bang rocks together make package tracker bot",
    intents=intents
)

helpmenu = DefaultMenu("◀️", "▶️", "❌")
bot.help_command = PrettyHelp(
    no_category="Commands", navigation=helpmenu, color=discord.Colour.blurple()
)

@bot.command()
async def distrohop(ctx, *, count=None):
    """Count another miku distrohop"""
    if os.path.exists("miku_distrohops.txt"):
        with open("miku_distrohops.txt", "r") as f:
            distrohops = int(f.read())
    else:
        distrohops = 0
    if count != None:
        distrohops += int(count)
    with open("miku_distrohops.txt", "w") as f:
        f.write(str(distrohops))
    await ctx.send("Miku distrohops: " + str(distrohops))

@bot.event
async def on_ready():
    chan = bot.get_channel(842491569176051712)
    cogs_dir = "cogs"
    for extension in [f.replace(".py", "") for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (Exception) as e:
            await chan.send(f"Failed to load extension `{extension}`, reason was:")
            await chan.send("```" + str(e) + "```")

    await chan.send("Started/restarted at: `" + str(datetime.now()) + "`")

if not os.path.exists(os.environ["HOME"] + "/.cavetoken"):
    print("No token found")
    exit()
else:
    token = open(os.environ["HOME"] + "/.cavetoken", "r").read()
    bot.run(token)
