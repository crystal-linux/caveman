import sys, datetime, os

import discord
from discord.ext import commands, tasks
import feedparser,requests

from global_config import configboi

from util_functions import *

sc = configboi("config.txt", False)
REFRESH_TIME = sc.getasint("REFRESH_TIME")

class RSS(commands.Cog):
    """This cog handles RSS stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)

        self.package_names = self.confmgr.getaslist("WATCHED_PACKAGES")
        temp = self.confmgr.getaslist("FEED_URLS")
        self.gitea_urls = self.confmgr.getaslist("GITEA_URLS")
        self.package_channel = self.confmgr.getasint("PACKAGE_CHANNEL")


        self.feed_urls = []
        for feed in temp:
            self.feed_urls.append("https://" + feed)

        self.chan = self.bot.get_channel(self.package_channel)
        if self.chan is None:
            syslog.log("RSS", "Package task failed because we couldn't find the target channel.")
            sys.exit(1)

        self.root = "package-cache"
        ensure(self.root)

        self.package_task.start()


    def cog_unload(self):
        self.package_task.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        syslog.log("RSS", "Running initial package check")
        await self.check_packages()

    @tasks.loop(seconds=REFRESH_TIME)
    async def package_task(self):
        await self.check_packages()

    @package_task.before_loop
    async def before_status_task(self):
        syslog.log(
            "RSS", "Waiting for bot to be ready before starting package task"
        )
        await self.bot.wait_until_ready()
        syslog.log("RSS", "Bot is ready. Enabling package task")

    async def sendwarn(self, msg):
        await self.chan.send(embed=warnmsg("RSS",msg))

    async def senderr(self, msg):
        await self.chan.send(embed=errmsg("RSS",msg))

    async def send(self, msg):
        await self.chan.send(embed=infmsg("RSS",msg))

    def dolog(self, msg):
        syslog.log("RSS", msg)

    async def check_packages(self):
        try:
            for feed in self.feed_urls:
                self.dolog("Checking: " + feed)
                previous = ""
                if check(self.root + "/" + feed.replace("/","-")):
                    self.dolog("Found previous cached data")
                    previous = open(self.root + "/" + feed.replace("/","-")).read().strip()
                else:
                    self.dolog("No previous data")

                new = requests.get(feed).text

                if new != previous:
                    self.dolog("New data is different")
                    if check(self.root + "/" + feed.replace("/","-")):
                        os.remove(self.root + "/" + feed.replace("/","-"))
                    with open(self.root + "/" + feed.replace("/","-"), "w") as f:
                        f.write(new)
                    self.dolog("Updated cache")

                    d = feedparser.parse(new)
                    hadNew = False

                    for item in d.entries:
                        for tgt in self.package_names:
                            if tgt in str(item['title']):
                                await self.send("Package change: `" + str(item['title']) + "`")
                                hadNew = True
                                break
                    
                    if not hadNew:
                        await self.send("No package changes to report :)")

                else:
                    await self.send("No package changes to report :)")
        except Exception as e:
            syslog.log("RSS ERROR", str(e))


def setup(bot):
    bot.add_cog(RSS(bot))
