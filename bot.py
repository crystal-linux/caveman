# Standard python imports
import os, string, unicodedata, sys, re, random, time, datetime, subprocess, json, traceback
import urllib.parse
import importlib

from os import listdir
from os.path import isfile, join

# Pycord
import discord
from discord.ext import commands

# Kind've discord related
from pretty_help import DefaultMenu, PrettyHelp

# Other pip packages
import asyncio
import requests

# My own classes n such
from global_config import configboi
from util_functions import *

if os.path.sep == "\\":
    print("This bot is only supported on UNIX-like systems. Aborting.")
    sys.exit(1)

intents = discord.Intents.default()
intents.members = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(";"),
    description="Ooga booga hit rocks together",
    intents=intents,
)

helpmenu = DefaultMenu("◀️", "▶️", "❌")
bot.help_command = PrettyHelp(
    no_category="Commands", navigation=helpmenu, color=discord.Colour.blurple()
)

# Sane default?
my_homedir = os.getenv("HOME", "/home/caveman")

# No default b/c we're fucked long before this if PATH is none
old_path = os.getenv("PATH")
new_path = old_path + ":" + my_homedir + "/.local/bin/"
os.environ["PATH"] = new_path

print("Our PATH is: " + os.getenv("PATH"))

# Startup event
@bot.event
async def on_ready():
    syslog.log("Main-Important", "Bot has restarted at " + getstamp())
    syslog.log("Main", f"\n{bot.user} has connected to Discord!\n")

    if check("restarted.txt"):
        channel = get("restarted.txt")
        chan = bot.get_channel(int(channel))
        if chan is not None:
            await chan.send(
                embed=infmsg("System", "Finished restarting at: `" + getstamp() + "`")
            )
        os.remove("restarted.txt")

    ownerman = await bot.fetch_user(OWNER)

    notifyowner = confmgr.getasbool("OWNER_DM_RESTART")

    cogs_dir = "cogs"
    for extension in [
        f.replace(".py", "") for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))
    ]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            syslog.log("Main", "Loaded " + extension)
            # await ownerman.send(embed=infmsg("System","Loaded `" + extension + "`"))
        except (Exception) as e:
            await ownerman.send(
                embed=errmsg(
                    "System", "Error from cog: " + extension + ": ```" + str(e) + "```"
                )
            )
            syslog.log("Main", f"Failed to load extension {extension}.")
            # traceback.print_exc()

    if notifyowner:
        await ownerman.send(
            embed=infmsg("System", "Started/restarted at: `" + getstamp() + "`")
        )


@bot.event
async def on_message(message):

    if message.author != bot.user:

        mc = message.content
        if "bot" in mc:
            # we're being talked to
            if "bad" in mc or "sucks" in mc:
                await message.channel.send(":(")

        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    syslog.log("Main", "Error in command: " + str(error))
    await ctx.send(embed=errmsg("Error", "```" + str(error) + "```"))


@bot.command()
async def removecog(ctx, name):
    """Un-load a cog that was loaded by default."""
    if ctx.message.author.id == OWNER:
        await ctx.send(embed=infmsg("Gotcha", "Ok, I'll try to disable `" + name + "`"))
        try:
            bot.remove_cog(name)
            syslog.log("Main", "Disabled cog: " + name)
            await ctx.send(embed=warnmsg("Done", "Disabled: `" + name + "`."))
        except Exception as e:
            await ctx.send(
                embed=errmsg("Broke", "Something went wrong: `" + str(e) + "`.")
            )
    else:
        await ctx.send(embed=errmsg("Oops", wrongperms("removecog")))


@bot.command()
async def getsyslog(ctx):
    """Get a copy of the system log"""
    if ctx.message.author.id == OWNER:
        log = syslog.getlog()
        if len(log) > 1994:
            text = paste(log)
            await ctx.send(embed=infmsg("Output", text))
        else:
            text = "```" + log + "```"
            await ctx.send("Here you go:")
            await ctx.send(text)
    else:
        await ctx.send(embed=errmsg("Oops", wrongperms("getsyslog")))


if UNLOAD_COGS is not None:
    # Remove any cogs as per config
    for item in UNLOAD_COGS:
        if item != "" and item != " ":
            syslog.log("Main", "Trying to remove '" + item + "'")
            try:
                bot.remove_cog(item)
                syslog.log("Main", "Removed '" + item + "'")
            except:
                syslog.log("Main", "Failed to remove '" + item + "'")


if check(".cavetoken"):
    token = open(".cavetoken").read().strip()
else:
    fail("No token found in .cavetoken")

bot.run(token)