from datetime import date
from unittest.mock import AsyncMock, Mock

import pytest

from discord_habit_tracker.models.tracker_member import TrackerMember
from discord_habit_tracker.services.reminder_eligibility_service import (
    ReminderEligibilityService,
)


@pytest.fixture
def dependencies():
    """Create mocked dependencies for reminder eligibility tests."""

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(
        return_value=TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
            reminders_enabled=True,
        )
    )

    current_date_resolver = Mock()
    current_date_resolver.resolve.return_value = date(2026, 10, 22)

    activity_repository = Mock()
    activity_repository.has_activity_for_date = AsyncMock(
        return_value=False
    )

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock(
        return_value=5
    )

    delivery_repository = Mock()
    delivery_repository.has_delivery = AsyncMock(
        return_value=False
    )

    service = ReminderEligibilityService(
        membership_repository=membership_repository,
        current_date_resolver=current_date_resolver,
        activity_repository=activity_repository,
        activity_stats_service=activity_stats_service,
        delivery_repository=delivery_repository,
    )

    return {
        "service": service,
        "membership_repository": membership_repository,
        "current_date_resolver": current_date_resolver,
        "activity_repository": activity_repository,
        "activity_stats_service": activity_stats_service,
        "delivery_repository": delivery_repository,
    }


@pytest.mark.asyncio
async def test_member_is_eligible_when_all_conditions_are_met(dependencies):
    """Test that an opted-in member with an active streak is eligible."""

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is True

    dependencies["membership_repository"].get_member.assert_awaited_once_with(
        999,
        12345,
    )

    dependencies["current_date_resolver"].resolve.assert_called_once_with(
        "Asia/Singapore",
    )

    dependencies["activity_repository"].has_activity_for_date.assert_awaited_once_with(
        999,
        12345,
        date(2026, 10, 22),
    )

    dependencies["activity_stats_service"].get_current_streak.assert_awaited_once_with(
        999,
        12345,
        date(2026, 10, 22),
    )

    dependencies["delivery_repository"].has_delivery.assert_awaited_once_with(
        999,
        12345,
        "2026-10-22",
    )


@pytest.mark.asyncio
async def test_member_is_ineligible_when_reminders_are_disabled(dependencies):
    """Test that members who have not opted in are excluded."""

    dependencies["membership_repository"].get_member.return_value = (
        TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
            reminders_enabled=False,
        )
    )

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is False

    dependencies["activity_repository"].has_activity_for_date.assert_not_awaited()
    dependencies["activity_stats_service"].get_current_streak.assert_not_awaited()
    dependencies["delivery_repository"].has_delivery.assert_not_awaited()


@pytest.mark.asyncio
async def test_member_is_ineligible_when_current_streak_is_zero(dependencies):
    """Test that members without a current streak are excluded."""

    dependencies["activity_stats_service"].get_current_streak.return_value = 0

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is False

    dependencies["delivery_repository"].has_delivery.assert_not_awaited()


@pytest.mark.asyncio
async def test_member_is_ineligible_when_already_active_today(dependencies):
    """Test that members who have already recorded activity are excluded."""

    dependencies["activity_repository"].has_activity_for_date.return_value = True

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is False

    dependencies["activity_stats_service"].get_current_streak.assert_not_awaited()
    dependencies["delivery_repository"].has_delivery.assert_not_awaited()


@pytest.mark.asyncio
async def test_member_is_ineligible_when_reminder_was_already_delivered(
    dependencies,
):
    """Test that members are not reminded twice on the same local date."""

    dependencies["delivery_repository"].has_delivery.return_value = True

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is False


@pytest.mark.asyncio
async def test_non_member_is_ineligible(dependencies):
    """Test that users who are not tracker members are excluded."""

    dependencies["membership_repository"].get_member.return_value = None

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is False

    dependencies["current_date_resolver"].resolve.assert_not_called()
    dependencies["activity_repository"].has_activity_for_date.assert_not_awaited()
    dependencies["activity_stats_service"].get_current_streak.assert_not_awaited()
    dependencies["delivery_repository"].has_delivery.assert_not_awaited()


@pytest.mark.asyncio
async def test_member_timezone_determines_the_reminder_date(dependencies):
    """Test that the member's configured timezone determines their date."""

    dependencies["membership_repository"].get_member.return_value = (
        TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="America/Los_Angeles",
            reminders_enabled=True,
        )
    )

    dependencies["current_date_resolver"].resolve.return_value = date(
        2026, 10, 21
    )

    result = await dependencies["service"].is_eligible(999, 12345)

    assert result is True

    dependencies["current_date_resolver"].resolve.assert_called_once_with(
        "America/Los_Angeles",
    )

    dependencies["activity_repository"].has_activity_for_date.assert_awaited_once_with(
        999,
        12345,
        date(2026, 10, 21),
    )

    dependencies["delivery_repository"].has_delivery.assert_awaited_once_with(
        999,
        12345,
        "2026-10-21",
    )
