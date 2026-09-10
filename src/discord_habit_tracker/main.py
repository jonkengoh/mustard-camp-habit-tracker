import asyncio

from discord_habit_tracker.config import Config
from discord_habit_tracker.discord_gateway import DiscordGateway
from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.repositories.message_repository import MessageRepository



async def main():
    """Application entry point."""

    config = Config()

    repository = MessageRepository()

    listener = EventListener(
        repository,
        config.tracked_user_id,
    )

    gateway = DiscordGateway(
        config.bot_token,
        listener.handle_message,
    )

    await gateway.start()


if __name__ == "__main__":
    asyncio.run(main())
