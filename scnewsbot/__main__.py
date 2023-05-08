import tomllib
import os
from dotenv import load_dotenv
from bot import Bot
from utils import Config


class InvalidTokenException(Exception):
    pass


class InvalidConfigException(Exception):
    pass


def main() -> None:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        raise InvalidTokenException("A Discord token was not set.")

    with open("config.toml", "rb") as config_file:
        if "[permissions]" in config_file.read():
            raise InvalidConfigException(
                "The format for permissions has changed; please check the new example config."
            )

        config = Config(tomllib.load(config_file))

    bot = Bot(config)
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    load_dotenv()
    main()
