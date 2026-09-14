import asyncio

from discord_habit_tracker.config import Config
from discord_habit_tracker.discord_gateway import DiscordGateway
from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.repositories.activity_repository import ActivityRepository
from discord_habit_tracker.services.activity_qualification_service import (
    ActivityQualificationService,
)


async def main():
    """Application entry point."""

    config = Config()

    activity_repository = ActivityRepository()
    qualification_service = ActivityQualificationService()

    listener = EventListener(
        activity_repository,
        config.tracked_user_id,
        qualification_service,
    )

    gateway = DiscordGateway(
        config.bot_token,
        listener.handle_message,
    )

    await gateway.start()


if __name__ == "__main__":
    asyncio.run(main())
