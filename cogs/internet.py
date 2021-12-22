import os, json, random
import urllib.parse
import urllib

import discord
from discord.ext import commands
import asyncio

from util_functions import *
from global_config import configboi

# Fun internet things
class Internet(commands.Cog):
    """Useful tools on the interwebs"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)

    async def getasjson(self, url):
        try:
            data = await run_command_shell('curl "' + url + '"')
            return json.loads(data)
        except Exception as e:
            return '{"haha":"heeho"}'

    @commands.command()
    async def kernel(self, ctx):
        """Get Linux kernel info for host and latest"""
        try:
            await ctx.send(embed=infmsg("Kernel", "Getting kernel info."))
            data = await self.getasjson("https://www.kernel.org/releases.json")
            new_ver = data["latest_stable"]["version"]
            mine = await run_command_shell("uname -r")
            msg = (
                "I'm running: `"
                + mine
                + "`\nKernel.org reports stable is: `"
                + new_ver
                + "`"
            )
            await ctx.send(embed=infmsg("Kernel", msg))
        except Exception as e:
            await ctx.send(
                embed=errmsg("Kernel", "Had an issue getting info: `" + str(e) + "`")
            )
            syslog.log("Internet-Important", "Kernel command had error: " + str(e))

# End fun internet things
def setup(bot):
    bot.add_cog(Internet(bot))
