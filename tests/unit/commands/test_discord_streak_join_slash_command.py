from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.commands.discord_streak_join_slash_command import (
    DiscordStreakJoinSlashCommand,
)
from discord_habit_tracker.commands.timezone_select_view import (
    TimezoneSelectView,
)


async def test_join_command_presents_timezone_selector():
    membership_service = Mock()

    command = DiscordStreakJoinSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    interaction.response.send_message.assert_awaited_once()

    _, kwargs = interaction.response.send_message.call_args

    assert isinstance(kwargs["view"], TimezoneSelectView)


async def test_join_command_prompts_user_to_select_timezone():
    membership_service = Mock()

    command = DiscordStreakJoinSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "Select your timezone to join the tracker.",
        view=interaction.response.send_message.call_args.kwargs["view"],
    )


