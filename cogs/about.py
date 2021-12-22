import discord
from discord.ext import commands

from util_functions import *

# Hopefully we'll never need logging here


class About(commands.Cog):
    """Stuff that the developer couldn't find a better category for"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        """Bot source code link"""
        await ctx.send(
            embed=infmsg(
                "Source",
                "My source code lives here: https://git.getcryst.al/crystal/caveman",
            )
        )

    @commands.command()
    async def report(self, ctx):
        """Report bot issues"""
        await ctx.send(
            embed=infmsg(
                "Issues",
                "You can file issues here: https://git.getcryst.al/crystal/caveman/issues",
            )
        )

    @commands.command()
    async def suggest(self, ctx):
        """Suggest bot feature(s)"""
        await ctx.send(
            embed=infmsg(
                "Issues",
                "You can file issues here: https://git.getcryst.al/crystal/caveman/issues",
            )
        )

    @commands.command()
    async def version(self, ctx):
        """Bot version"""
        commit_msg = await run_command_shell(
            "git --no-pager log --decorate=short --pretty=oneline -n1"
        )
        msg = ""
        msg += "Latest Git commit: \n"
        msg += "```" + commit_msg + "```"
        await ctx.send(embed=infmsg("Bot Stats", msg))

    @commands.command()
    async def invite(self, ctx):
        """Add me to another server"""
        await ctx.send(
            embed=infmsg(
                "Invite me :)",
                "https://discord.com/api/oauth2/authorize?client_id=900841588996063282&permissions=8&scope=bot%20applications.commands",
            )
        )


def setup(bot):
    bot.add_cog(About(bot))
