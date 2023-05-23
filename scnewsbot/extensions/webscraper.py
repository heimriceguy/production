import hashlib
import urllib3
import random
import time
from discord.ext import commands
import discord


url = "http://raw.adventuresintechland.com/freedom.html"
sleeptime = 60


class WebscraperCog(commands.Cog, name="Webscraper"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def getHash():
        randomint = random.randint(0,7)

        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
        ]

        http = urllib3.PoolManager()
        request = http.request(
            "GET",
            url,
            headers = {
                "User-agent": user_agents[randomint]
            }
        )

        return hashlib.sha224(request.data).hexdigest()

    current_hash = getHash()

    while 1:
        if getHash() == current_hash:
            next
        else:
            print("Changed")
            break
        time.sleep(sleeptime)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WebscraperCog(bot))