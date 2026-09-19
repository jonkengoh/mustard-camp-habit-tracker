import asyncio

from pathlib import Path
from discord_habit_tracker.config import Config
from discord_habit_tracker.discord_gateway import DiscordGateway
from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.repositories.sqlite_activity_repository import SQLiteActivityRepository
from discord_habit_tracker.services.activity_qualification_service import ActivityQualificationService
from discord_habit_tracker.services.activity_date_resolver import ActivityDateResolver
from discord_habit_tracker.commands.streak_command import StreakCommand
from discord_habit_tracker.services.activity_stats_service import ActivityStatsService
from discord_habit_tracker.services.streak_service import StreakService



async def main():
    """Application entry point."""

    config = Config()

    # Initialize application dependencies
    data_directory = Path("data")
    data_directory.mkdir(exist_ok=True)

    activity_repository = SQLiteActivityRepository(
        str(data_directory / "activity_tracker.db")
    )

    qualification_service = ActivityQualificationService()

    date_resolver = ActivityDateResolver()

    streak_service = StreakService()

    activity_stats_service = ActivityStatsService(
        activity_repository,
        streak_service,
    )

    streak_command = StreakCommand(
        activity_stats_service,
    )

    # Initialize the event listener and Discord gateway
    listener = EventListener(
        activity_repository,
        config.tracked_user_id,
        qualification_service,
        date_resolver,
        config.tracked_user_timezone,
    )

    gateway = DiscordGateway(
        config.bot_token,
        listener.handle_message,
        streak_command,
        config.tracked_user_timezone,
    )

    try:
        await gateway.start()
    finally:
        activity_repository.close()


if __name__ == "__main__":
    asyncio.run(main())
