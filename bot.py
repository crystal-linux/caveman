import discord,os
from discord.ext import commands

from task import Packages

bot = commands.Bot(";")
bot.add_cog(Packages(bot))


@bot.command()
async def distrohop(self, ctx, *, count=0):
    """Count another miku distrohop"""
    if os.path.exists("miku_distrohops.txt"):
        with open("miku_distrohops.txt", "r") as f:
            distrohops = int(f.read())
    else:
        distrohops = 0
    distrohops += count
    with open("miku_distrohops.txt", "w") as f:
        f.write(str(distrohops))
    await ctx.send("Miku distrohops: " + str(distrohops))

if not os.path.exists(os.environ["HOME"] + "/.cavetoken"):
    print("No token found")
    exit()
else:
    token = open(os.environ["HOME"] + "/.cavetoken", "r").read()
    bot.run(token)