from datetime import datetime
from unittest.mock import AsyncMock, Mock
from zoneinfo import ZoneInfo

from discord_habit_tracker.models.tracker_member import TrackerMember
from discord_habit_tracker.services.daily_reminder_scheduler import (
    DailyReminderScheduler,
)


async def test_sends_and_records_reminder_for_eligible_member_at_scheduled_time():
    """Send and record a reminder when an eligible member is due."""

    member = TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
        reminders_enabled=True,
    )

    membership_repository = Mock()
    membership_repository.get_members_with_reminders_enabled = AsyncMock(
        return_value=[member],
    )

    eligibility_service = Mock()
    eligibility_service.is_eligible = AsyncMock(return_value=True)

    notifier = Mock()
    notifier.notify_reminder = AsyncMock()

    delivery_repository = Mock()
    delivery_repository.record_delivery = AsyncMock()

    guild = Mock()
    guild.id = 999

    discord_client = Mock()
    discord_client.get_guild.return_value = guild

    clock = Mock()
    clock.now.return_value = datetime(
        2026,
        10,
        24,
        21,
        0,
        tzinfo=ZoneInfo("Asia/Singapore"),
    )

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock(return_value=4)

    scheduler = DailyReminderScheduler(
        membership_repository=membership_repository,
        eligibility_service=eligibility_service,
        notifier=notifier,
        delivery_repository=delivery_repository,
        discord_client=discord_client,
        activity_stats_service=activity_stats_service,
        clock=clock,
    )

    await scheduler.check_reminders()

    eligibility_service.is_eligible.assert_awaited_once_with(999, 12345)
    notifier.notify_reminder.assert_awaited_once_with(
        guild,
        user_id=12345,
        current_streak=4,
    )
    delivery_repository.record_delivery.assert_awaited_once_with(
        999,
        12345,
        "2026-10-24",
    )


async def test_skips_reminder_when_member_is_not_eligible():
    """Do not send a reminder to an ineligible member."""

    member = TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
        reminders_enabled=True,
    )

    membership_repository = Mock()
    membership_repository.get_members_with_reminders_enabled = AsyncMock(
        return_value=[member],
    )

    eligibility_service = Mock()
    eligibility_service.is_eligible = AsyncMock(return_value=False)

    notifier = Mock()
    notifier.notify_reminder = AsyncMock()

    delivery_repository = Mock()
    delivery_repository.record_delivery = AsyncMock()

    discord_client = Mock()

    clock = Mock()
    clock.now.return_value = datetime(
        2026,
        10,
        24,
        21,
        0,
        tzinfo=ZoneInfo("Asia/Singapore"),
    )

    activity_stats_service = Mock()

    scheduler = DailyReminderScheduler(
        membership_repository=membership_repository,
        eligibility_service=eligibility_service,
        notifier=notifier,
        delivery_repository=delivery_repository,
        discord_client=discord_client,
        activity_stats_service=activity_stats_service,
        clock=clock,
    )

    await scheduler.check_reminders()

    eligibility_service.is_eligible.assert_awaited_once_with(999, 12345)
    notifier.notify_reminder.assert_not_awaited()
    delivery_repository.record_delivery.assert_not_awaited()


import pytest


async def test_does_not_record_delivery_when_notification_fails():
    """Do not record a delivery if sending the reminder fails."""

    member = TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
        reminders_enabled=True,
    )

    membership_repository = Mock()
    membership_repository.get_members_with_reminders_enabled = AsyncMock(
        return_value=[member],
    )

    eligibility_service = Mock()
    eligibility_service.is_eligible = AsyncMock(return_value=True)

    notifier = Mock()
    notifier.notify_reminder = AsyncMock(
        side_effect=RuntimeError("Discord send failed"),
    )

    delivery_repository = Mock()
    delivery_repository.record_delivery = AsyncMock()

    guild = Mock()
    discord_client = Mock()
    discord_client.get_guild.return_value = guild

    clock = Mock()
    clock.now.return_value = datetime(
        2026,
        10,
        24,
        21,
        0,
        tzinfo=ZoneInfo("Asia/Singapore"),
    )

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock(return_value=4)

    scheduler = DailyReminderScheduler(
        membership_repository=membership_repository,
        eligibility_service=eligibility_service,
        notifier=notifier,
        delivery_repository=delivery_repository,
        discord_client=discord_client,
        activity_stats_service=activity_stats_service,
        clock=clock,
    )

    with pytest.raises(RuntimeError, match="Discord send failed"):
        await scheduler.check_reminders()

    delivery_repository.record_delivery.assert_not_awaited()


async def test_skips_reminder_when_scheduled_time_has_passed():
    """Do not send a reminder long after its scheduled time."""

    member = TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
        reminders_enabled=True,
    )

    membership_repository = Mock()
    membership_repository.get_members_with_reminders_enabled = AsyncMock(
        return_value=[member],
    )

    eligibility_service = Mock()
    eligibility_service.is_eligible = AsyncMock(return_value=True)

    notifier = Mock()
    notifier.notify_reminder = AsyncMock()

    delivery_repository = Mock()
    delivery_repository.record_delivery = AsyncMock()

    discord_client = Mock()
    discord_client.get_guild.return_value = Mock()

    clock = Mock()
    clock.now.return_value = datetime(
        2026,
        10,
        24,
        22,
        0,
        tzinfo=ZoneInfo("Asia/Singapore"),
    )

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock(return_value=4)

    scheduler = DailyReminderScheduler(
        membership_repository=membership_repository,
        eligibility_service=eligibility_service,
        notifier=notifier,
        delivery_repository=delivery_repository,
        discord_client=discord_client,
        activity_stats_service=activity_stats_service,
        clock=clock,
    )

    await scheduler.check_reminders()

    notifier.notify_reminder.assert_not_awaited()
    delivery_repository.record_delivery.assert_not_awaited()
