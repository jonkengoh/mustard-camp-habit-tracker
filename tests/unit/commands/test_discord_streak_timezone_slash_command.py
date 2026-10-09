from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.commands.discord_streak_timezone_slash_command import (
    DiscordStreakTimezoneSlashCommand,
)
from discord_habit_tracker.commands.timezone_update_select_view import (
    TimezoneUpdateSelectView,
)


async def test_timezone_command_presents_timezone_update_selector():
    membership_service = Mock()

    command = DiscordStreakTimezoneSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    interaction.response.send_message.assert_awaited_once()

    _, kwargs = interaction.response.send_message.call_args

    assert isinstance(kwargs["view"], TimezoneUpdateSelectView)


async def test_timezone_command_prompts_user_to_select_new_timezone():
    membership_service = Mock()

    command = DiscordStreakTimezoneSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "Select your new timezone.",
        view=interaction.response.send_message.call_args.kwargs["view"],
    )
