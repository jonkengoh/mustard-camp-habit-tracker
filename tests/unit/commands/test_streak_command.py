from datetime import date
from unittest.mock import AsyncMock, Mock

import pytest

from discord_habit_tracker.commands.streak_command import StreakCommand


@pytest.mark.asyncio
async def test_streak_command_returns_current_and_longest_streak():
    """Test that the streak command returns both streak statistics."""

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock(return_value=5)
    activity_stats_service.get_longest_streak = AsyncMock(return_value=12)
    activity_stats_service.get_recent_activity_stats = AsyncMock(
        return_value={
            "active_days": 22,
            "total_days": 30,
            "activity_rate": 73.33333333333333,
        }
    )

    command = StreakCommand(
        activity_stats_service,
    )

    result = await command.handle(
        guild_id=999,
        user_id=12345,
        current_date=date(2026, 9, 20),
    )

    assert result == (
        "Current streak: 5 days\n"
        "Longest streak: 12 days\n"
        "Last 30 days: 22/30 active days (73.3%)"
    )

    activity_stats_service.get_current_streak.assert_awaited_once_with(
        999,
        12345,
        date(2026, 9, 20),
    )

    activity_stats_service.get_longest_streak.assert_awaited_once_with(
        999,
        12345,
    )

    activity_stats_service.get_recent_activity_stats.assert_awaited_once_with(
        999,
        12345,
        date(2026, 9, 20),
    )
