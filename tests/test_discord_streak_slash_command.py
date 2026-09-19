from datetime import date
from unittest.mock import AsyncMock, Mock

import pytest

from discord_habit_tracker.commands import streak_command
from discord_habit_tracker.commands.discord_streak_slash_command import (
    DiscordStreakSlashCommand,
)
from discord_habit_tracker.services import current_date_resolver


@pytest.mark.asyncio
async def test_streak_slash_command_responds_with_streaks():
    """Test that the slash command responds with the user's streaks."""

    interaction = Mock()
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    streak_command = Mock()
    streak_command.handle = AsyncMock(
        return_value="Current streak: 5 days\nLongest streak: 12 days"
    )

    current_date_resolver = Mock()
    current_date_resolver.resolve.return_value = date(2026, 9, 20)

    handler = DiscordStreakSlashCommand(
        streak_command,
        current_date_resolver,
        "Asia/Singapore",
    )


    await handler.handle(
        interaction,
    )

    current_date_resolver.resolve.assert_called_once_with(
        "Asia/Singapore",
    )

    streak_command.handle.assert_awaited_once_with(
        12345,
        date(2026, 9, 20),
    )

    interaction.response.send_message.assert_awaited_once_with(
        "Current streak: 5 days\nLongest streak: 12 days"
    )
