import asyncio

from discord_habit_tracker.config import Config
from discord_habit_tracker.discord_gateway import DiscordGateway


async def main():
    """Application entry point."""

    config = Config()

    gateway = DiscordGateway(config.bot_token)

    await gateway.start()


if __name__ == "__main__":
    asyncio.run(main())
