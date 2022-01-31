# Pip
from discord.ext import tasks, commands

# Stdlib
import feedparser,os

# Custom
from fancy import *

CHAN = 842491569176051712
ROLE = 825474723948265474
WATCHED = "grub,arch-install-scripts,base,filesystem,lsb-release,neofetch,pfetch"

class Package:
    def __init__(self,name,ver,arch):
        self.name = name
        self.ver = ver
        self.arch = arch
    def __str__(self):
        return self.name + ' ' + self.ver + ' ' + self.arch
    def __repr__(self):
        return self.__str__()


class Packages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check.start()
        if not os.path.exists("packages"):
            os.makedirs("packages")

    def cog_unload(self):
        self.check.cancel()

    @tasks.loop(seconds=300)
    async def check(self):
        watched = WATCHED.split(",")
        new = []

        feed_data = feedparser.parse('https://archlinux.org/feeds/packages/')

        for entry in feed_data.entries:
            info = entry.title
            name,version,arch = info.split(" ")
            if name in watched:
                p = Package(name,version,arch)
                new.append(p)

        for p in new:
            if os.path.exists("packages/" + p.name):
                ver = open("packages/" + p.name, "r").read()
                if ver != p.ver:
                    os.remove("packages/" + p.name)
                    with open("packages/" + p.name, "w") as f:
                        f.write(p.ver)
                else:
                    new.pop(p)
            else:
                with open("packages/" + p.name, "w") as f:
                        f.write(p.ver)

        if new != []:
            await self.bot.get_channel(CHAN).send("<@&" + str(ROLE) + ">, there are package changes.")
            for p in new:
                print(str(p))
                print("-"*10)
                msg = "`" + p.name + "` is now `" + p.ver + "`"
                await self.bot.get_channel(CHAN).send(embed=infmsg("New package",msg))
        #else:
        #    await self.bot.get_channel(CHAN).send(embed=infmsg("Notice","No new packages","Lucky for us :)"))

    @check.before_loop
    async def before_check(self):
        print('waiting for bot to be ready...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Packages(bot))
