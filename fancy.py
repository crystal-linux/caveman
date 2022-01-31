import discord

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