import subprocess
from discord.ext import commands
import discord
from utils import Config

VERSION = "0.0.0"
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True


class Bot(commands.Bot):
    def __init__(self, config: Config, /) -> None:
        super().__init__(
            intents=INTENTS,
            command_prefix=commands.when_mentioned_or(config.prefix),
            allowed_mentions=discord.AllowedMentions(everyone=False),
            case_insensitive=True,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="the devs..."
            ),
        )
        self.config = config
        self.version = VERSION

    async def setup_hook(self) -> None:
        for extension in self.config.extensions:
            await self.load_extension(extension)

        await self.add_cog(CoreCog(self))


class CoreCog(commands.Cog, name="Core"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def _get_version(self) -> str:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print ("The SC News Bot is online.")

    @commands.hybrid_command(description="Shows you some info about the bot.")
    async def info(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            color=self.bot.config.embed_color,
            description="SCNewsBot is a Discord bot created for the r/starcitizen\n Discord server to help with writing news posts.",
        )
        embed.add_field(
            name="Version", value=f"v{self.bot.version}+{self._get_version()}"
        )
        embed.add_field(
            name="Library", value=f"discord.py v{discord.__version__}", inline=False
        )
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Source Code",
                url="https://github.com/mudkipdev/scnewsbot",
                style=discord.ButtonStyle.link,
            )
        )
        await ctx.reply(embed=embed, view=view, mention_author=False)

    @commands.hybrid_command(description="Gives you instructions about using the embed creator.")
    async def instructions(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            color=self.bot.config.embed_color,
            title="Instructions",
            description="1. Title should not use any formatting.\n2. Youtube link should only be used for Youtube links or video links with pretty embeds.\n3. URL should be used for any regular link such as a comm-link.\n4. In the description box use `-` and it will replace it with ➣, use `+` and it will replace it with ✦ preceeded by three spaces.\n5. Use the `&ids` to get the channel and role IDs.\n6. Do not ping for every post if there are consecutive posts in the same channel, instead ping only on the final post and provide an overall preview.\n7. **ALWAYS** include a ping preview, you can find these using `&previews`.\n8. Always select publish unless explicitly not needed (server only announcements). ",
        )
        view = discord.ui.View()
        await ctx.reply(embed=embed, view=view, mention_author=False)
