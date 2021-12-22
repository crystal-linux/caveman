import discord
from discord.ext import commands

from util_functions import *

# Hopefully we'll never need logging here


class Random(commands.Cog):
    """Stuff that the developer couldn't find a better category for"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """pong."""
        await ctx.send(
            "pong. :upside_down: :gun:", file=discord.File("images/pong.jpg")
        )

def setup(bot):
    bot.add_cog(Random(bot))
