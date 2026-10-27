#!/usr/bin/env python3
import asyncio

# Standard Library
from pathlib import Path
from discord_habit_tracker.config import Config
from discord_habit_tracker.discord_gateway import DiscordGateway
from discord_habit_tracker.event_listener import EventListener

# Repositories
from discord_habit_tracker.repositories.sqlite_activity_repository import SQLiteActivityRepository
from discord_habit_tracker.repositories.sqlite_membership_repository import SQLiteMembershipRepository
from discord_habit_tracker.repositories.sqlite_reminder_delivery_repository import SQLiteReminderDeliveryRepository

# Services
from discord_habit_tracker.services.activity_qualification_service import ActivityQualificationService
from discord_habit_tracker.services.activity_date_resolver import ActivityDateResolver
from discord_habit_tracker.services.activity_stats_service import ActivityStatsService
from discord_habit_tracker.services.streak_service import StreakService
from discord_habit_tracker.services.membership_service import MembershipService
from discord_habit_tracker.adapters.discord_activity_notifier import DiscordActivityNotifier
from discord_habit_tracker.services.daily_reminder_scheduler import DailyReminderScheduler
from discord_habit_tracker.services.reminder_eligibility_service import ReminderEligibilityService
from discord_habit_tracker.services.current_date_resolver import CurrentDateResolver
from discord_habit_tracker.services.system_clock import SystemClock

# Commands
from discord_habit_tracker.commands.streak_command import StreakCommand
from discord_habit_tracker.commands.history_command import HistoryCommand


async def main():
    """Application entry point."""

    config = Config()

    # Initialize application dependencies
    data_directory = Path("data")
    data_directory.mkdir(exist_ok=True)

    database_path = str(data_directory / "activity_tracker.db")

    activity_repository = SQLiteActivityRepository(database_path)
    membership_repository = SQLiteMembershipRepository(database_path)

    membership_service = MembershipService(
        membership_repository,
    )

    reminder_delivery_repository = SQLiteReminderDeliveryRepository(
        database_path,
    )

    qualification_service = ActivityQualificationService()

    date_resolver = ActivityDateResolver()

    streak_service = StreakService()

    activity_notifier = DiscordActivityNotifier()

    activity_stats_service = ActivityStatsService(
        activity_repository,
        streak_service,
    )

    clock = SystemClock()

    reminder_eligibility_service = ReminderEligibilityService(
        membership_repository,
        CurrentDateResolver(),
        activity_repository,
        activity_stats_service,
        reminder_delivery_repository,
    )

    streak_command = StreakCommand(
        activity_stats_service,
    )

    history_command = HistoryCommand(
        activity_repository,
    )

    # Initialize the event listener and Discord gateway
    listener = EventListener(
        activity_repository,
        membership_repository,
        qualification_service,
        date_resolver,
    )

    gateway = DiscordGateway(
        config.bot_token,
        listener.handle_message,
        streak_command,
        history_command,
        membership_repository,
        membership_service,
        activity_stats_service=activity_stats_service,
        activity_notifier=activity_notifier,
    )

    reminder_scheduler = DailyReminderScheduler(
        membership_repository=membership_repository,
        eligibility_service=reminder_eligibility_service,
        notifier=activity_notifier,
        delivery_repository=reminder_delivery_repository,
        discord_client=gateway.client,
        activity_stats_service=activity_stats_service,
        clock=clock,
    )

    gateway.set_reminder_scheduler(reminder_scheduler)

    try:
        await gateway.start()
    finally:
        activity_repository.close()
        membership_repository.close()
        reminder_delivery_repository.close()


if __name__ == "__main__":
    asyncio.run(main())
