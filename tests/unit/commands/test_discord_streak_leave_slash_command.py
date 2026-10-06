from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.services.exceptions import MemberNotFoundError

from discord_habit_tracker.commands.discord_streak_leave_slash_command import (
    DiscordStreakLeaveSlashCommand,
)


async def test_leave_command_removes_user_from_tracker():
    membership_service = Mock()
    membership_service.leave = AsyncMock()

    command = DiscordStreakLeaveSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    membership_service.leave.assert_awaited_once_with(
        999,
        12345,
    )


async def test_leave_command_confirms_user_left_tracker():
    membership_service = Mock()
    membership_service.leave = AsyncMock()

    command = DiscordStreakLeaveSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "You've left the activity tracker."
    )


async def test_leave_command_rejects_non_member():
    membership_service = Mock()
    membership_service.leave = AsyncMock(
        side_effect=MemberNotFoundError,
    )

    command = DiscordStreakLeaveSlashCommand(
        membership_service,
    )

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    await command.handle(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "You're not participating in the tracker."
    )

