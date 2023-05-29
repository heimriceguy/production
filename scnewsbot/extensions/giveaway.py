import discord
from discord.ext import commands

class GiveawayCog(commands.Cog, name="Giveaway"):
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

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GiveawayCog(bot))