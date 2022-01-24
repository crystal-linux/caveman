import discord,os
from discord.ext import commands

from task import Packages

bot = commands.Bot(";")
bot.add_cog(Packages(bot))


if not os.path.exists(os.environ["HOME"] + "/.cavetoken"):
    print("No token found")
    exit()
else:
    token = open(os.environ["HOME"] + "/.cavetoken", "r").read()
    bot.run(token)