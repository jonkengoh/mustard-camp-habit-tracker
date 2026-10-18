from datetime import date
from unittest.mock import AsyncMock, Mock

import pytest

from discord_habit_tracker.services.activity_stats_service import (
    ActivityStatsService,
)


@pytest.mark.asyncio
async def test_activity_stats_service_calculates_current_streak():
    """Test that activity stats calculate the current streak."""

    activity_repository = Mock()
    activity_repository.get_activity_dates = AsyncMock(
        return_value={
            date(2026, 9, 16),
            date(2026, 9, 17),
            date(2026, 9, 18),
        }
    )

    streak_service = Mock()
    streak_service.calculate_current_streak.return_value = 3

    service = ActivityStatsService(
        activity_repository,
        streak_service,
    )

    result = await service.get_current_streak(
        999,
        12345,
        date(2026, 9, 18),
    )

    assert result == 3

    activity_repository.get_activity_dates.assert_awaited_once_with(
        999,
        12345,
    )

    streak_service.calculate_current_streak.assert_called_once_with(
        {
            date(2026, 9, 16),
            date(2026, 9, 17),
            date(2026, 9, 18),
        },
        date(2026, 9, 18),
    )

@pytest.mark.asyncio
async def test_activity_stats_service_calculates_longest_streak():
    """Test that activity stats calculate the longest streak."""

    activity_repository = Mock()
    activity_repository.get_activity_dates = AsyncMock(
        return_value={
            date(2026, 9, 10),
            date(2026, 9, 11),
            date(2026, 9, 13),
            date(2026, 9, 14),
            date(2026, 9, 15),
        }
    )

    streak_service = Mock()
    streak_service.calculate_longest_streak.return_value = 3

    service = ActivityStatsService(
        activity_repository,
        streak_service,
    )

    result = await service.get_longest_streak(
        999,
        12345,
    )

    assert result == 3

    activity_repository.get_activity_dates.assert_awaited_once_with(
        999,
        12345,
    )

    streak_service.calculate_longest_streak.assert_called_once_with(
        {
            date(2026, 9, 10),
            date(2026, 9, 11),
            date(2026, 9, 13),
            date(2026, 9, 14),
            date(2026, 9, 15),
        },
    )


@pytest.mark.asyncio
async def test_activity_stats_service_calculates_recent_activity_stats():
    """Test activity statistics over the last 30 calendar days."""
    activity_repository = Mock()
    activity_repository.get_activity_dates_in_range = AsyncMock(
        return_value={
            date(2026, 9, 20),
            date(2026, 10, 1),
            date(2026, 10, 18),
        }
    )

    streak_service = Mock()

    service = ActivityStatsService(
        activity_repository,
        streak_service,
    )

    result = await service.get_recent_activity_stats(
        guild_id=999,
        user_id=12345,
        current_date=date(2026, 10, 18),
    )

    assert result == {
        "active_days": 3,
        "total_days": 30,
        "activity_rate": pytest.approx(10.0),
    }

    activity_repository.get_activity_dates_in_range.assert_awaited_once_with(
        999,
        12345,
        date(2026, 9, 19),
        date(2026, 10, 18),
    )
