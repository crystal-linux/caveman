# Stdlib
import os
from datetime import datetime

# Pip
import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

# Custom
from fancy import *

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

@bot.event
async def on_ready():
    chan = bot.get_channel(842491569176051712)
    cogs_dir = "cogs"
    for extension in [f.replace(".py", "") for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (Exception) as e:
            await chan.send(embed=errmsg("Load error",f"Failed to load extension `{extension}`, traceback below."))
            await chan.send(embed=errmsg("Traceback","```" + str(e) + "```"))

    await chan.send("Started/restarted at: `" + str(datetime.now()) + "`")

if not os.path.exists(os.environ["HOME"] + "/.cavetoken"):
    print("No token found")
    exit()
else:
    token = open(os.environ["HOME"] + "/.cavetoken", "r").read()
    bot.run(token)
