# System
import os, sys, random, string

# Pip
import asyncio, requests, youtube_dl, discord

# Me
from global_config import configboi
from logger import BotLogger

# lol
confmgr = configboi("config.txt", False)
syslog = BotLogger("system_log.txt")

# <-------------- Don't touch pls --------------->
# If you're adding your own stuff, you need to look at
# global_config.py to see the supported data types, and add your
# own if needed.
# .get is string
VER = confmgr.get("VER")

HELP_LOC = confmgr.get("HELP_LOC")

WRONG_PERMS = confmgr.get("WRONG_PERMS")

NEW_MEMBER = confmgr.get("NEW_MEMBER")
INTRO_CHANNEL = confmgr.get("INTRO_CHANNEL")

DEFAULT_STATUS_TYPE = confmgr.get("DEFAULT_STATUS_TYPE")
DEFAULT_STATUS_TEXT = confmgr.get("DEFAULT_STATUS_TEXT")

UNLOAD_COGS = confmgr.getaslist("UNLOAD_COGS")
# <-------------- End --------------------->

# <--------------Colors Start-------------->
# For embed msgs (you can override these if you want)
# But changing the commands which use embed would be better
purple_dark = 0x6A006A
purple_medium = 0xA958A5
purple_light = 0xC481FB
orange = 0xFFA500
gold = 0xDAA520
red_dark = 8e2430
red_light = 0xF94343
blue_dark = 0x3B5998
cyan = 0x5780CD
blue_light = 0xACE9E7
aqua = 0x33A1EE
pink = 0xFF9DBB
green_dark = 0x2AC075
green_light = 0xA1EE33
white = 0xF9F9F6
cream = 0xFFDAB9
# <--------------Colors End-------------->

WHITELIST = []


def strip_dangerous(text):
    remove = [";", "&&", "&", '"']
    for thing in remove:
        text = text.replace(thing, "")

    if "\n" in text:
        text = text.split("\n")[0]

    return text


def fancymsg(title, text, color, footnote=None):

    e = discord.Embed(colour=color)
    e.add_field(name=title, value=text, inline=False)

    if footnote is not None:
        e.set_footer(text=footnote)

    return e


def errmsg(title, text, footnote=None):
    return fancymsg(title, text, discord.Colour.red(), footnote)


def warnmsg(title, text, footnote=None):
    return fancymsg(title, text, discord.Colour.gold(), footnote)


def infmsg(title, text, footnote=None):
    return fancymsg(title, text, discord.Colour.blurple(), footnote)


def imgbed(title, type, dat):
    # see https://discordpy.readthedocs.io/en/stable/faq.html?highlight=embed#how-do-i-use-a-local-image-file-for-an-embed-image
    e = discord.Embed(color=discord.Colour.blurple())
    e.add_field(name="foo", value=title, inline=False)
    if type == "rem":
        e.set_image(url=dat)
    else:
        e.set_image(url="attachment://" + dat)
    return e

# Simple file wrappers
def check(fn):
    if os.path.exists(fn):
        return True
    else:
        return False


def save(fn, text):
    with open(fn, "a+") as f:
        f.write(text + "\n")


def get(fn):
    if check(fn):
        with open(fn) as f:
            return f.read()

def ensure(fn):
    if not check(fn):
        os.makedirs(fn, exist_ok=True)


def getstamp():
    if sys.platform != "win32":
        os.system("date >> stamp")
        with open("stamp") as f:
            s = f.read()
        os.remove("stamp")
        return s
    else:
        return ""

def wrongperms(command):
    syslog.log("System", "Someone just failed to run: '" + command + "'")
    return WRONG_PERMS.replace("{command}", command)
