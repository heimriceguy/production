import discord
from discord.ext import commands
from googleapiclient.discovery import build
import asyncio
import requests

class AlerterCog(commands.Cog, name="Alerter"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description="Get list of users who reacted to a specific message.")
    async def reactlist(self, ctx, message: discord.Message) -> None:
        for reaction in message.reactions:
            users = [
                user async for user in reaction.users()
                if user != self.bot.user
            ]
        await message.channel.send(users)
        print ("test")

        client = discord.Client()

        TWITCH_CLIENT_ID = '2clwzhet0ewd7n6wkvem7jc5bzrc6w'
        TWITCH_USER_ID = '496533830'

        async def check_new_stream():
            url = f"https://api.twitch.tv/helix/streams?user_id={TWITCH_USER_ID}"
            headers = {"Client-ID": TWITCH_CLIENT_ID}
            response = requests.get(url, headers=headers).json()
            if response["data"]:
                stream_title = response["data"][0]["title"]
                stream_link = f"https://www.twitch.tv/{response['data'][0]['user_login']}"
                # Send message to Discord server
                channel = client.get_channel(1091152461844185158)
                await channel.send(f"{stream_title} is now live here: {stream_link}.")

        async def check_new_upload():
            url = f"https://api.twitch.tv/helix/videos?user_id={TWITCH_USER_ID}"
            headers = {"Client-ID": TWITCH_CLIENT_ID}
            response = requests.get(url, headers=headers).json()
            if response["data"]:
                video_title = response["data"][0]["title"]
                video_link = response["data"][0]["url"]
                # Send message to Discord server
                channel = client.get_channel(1091152461844185158)
                await channel.send(f"New Twitch video! '{video_title}' was uploaded here: {video_link}.")

        @commands.Cog.listener()
        async def on_ready():
            while True:
                await check_new_stream()
                await check_new_upload()
                await asyncio.sleep(600)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AlerterCog(bot)) 