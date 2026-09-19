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

    command = StreakCommand(
        activity_stats_service,
    )

    result = await command.handle(
        user_id=12345,
        current_date=date(2026, 9, 20),
    )

    assert result == "Current streak: 5 days\nLongest streak: 12 days"

    activity_stats_service.get_current_streak.assert_awaited_once_with(
        12345,
        date(2026, 9, 20),
    )

    activity_stats_service.get_longest_streak.assert_awaited_once_with(
        12345,
    )
