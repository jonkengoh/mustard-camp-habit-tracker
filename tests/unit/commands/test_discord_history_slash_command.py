from datetime import date
from unittest.mock import AsyncMock, Mock

import pytest

from discord_habit_tracker.commands.discord_history_slash_command import (
    DiscordHistorySlashCommand,
)
from discord_habit_tracker.models.tracker_member import TrackerMember


@pytest.mark.asyncio
async def test_history_command_defaults_to_seven_days():
    """Show the current day and previous six days by default."""

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    history_command = Mock()
    history_command.handle = AsyncMock(return_value="Activity History")

    current_date_resolver = Mock()
    current_date_resolver.resolve.return_value = date(2026, 10, 17)

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(
        return_value=TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
        )
    )

    command = DiscordHistorySlashCommand(
        history_command,
        current_date_resolver,
        membership_repository,
    )

    await command.handle(interaction)

    history_command.handle.assert_awaited_once_with(
        999,
        12345,
        date(2026, 10, 11),
        date(2026, 10, 17),
    )

    interaction.response.send_message.assert_awaited_once_with(
        "Activity History"
    )


@pytest.mark.asyncio
async def test_history_command_accepts_custom_period():
    """Use the requested number of days when supplied."""

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    history_command = Mock()
    history_command.handle = AsyncMock(return_value="Activity History")

    current_date_resolver = Mock()
    current_date_resolver.resolve.return_value = date(2026, 10, 17)

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(
        return_value=TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
        )
    )

    command = DiscordHistorySlashCommand(
        history_command,
        current_date_resolver,
        membership_repository,
    )

    await command.handle(interaction, days=30)

    history_command.handle.assert_awaited_once_with(
        999,
        12345,
        date(2026, 9, 18),
        date(2026, 10, 17),
    )


@pytest.mark.asyncio
async def test_history_command_rejects_period_outside_supported_range():
    """Reject a period outside the supported 1–30 day range."""

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    history_command = Mock()
    history_command.handle = AsyncMock()

    current_date_resolver = Mock()

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(
        return_value=TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
        )
    )

    command = DiscordHistorySlashCommand(
        history_command,
        current_date_resolver,
        membership_repository,
    )

    await command.handle(interaction, days=31)

    history_command.handle.assert_not_awaited()
    current_date_resolver.resolve.assert_not_called()

    interaction.response.send_message.assert_awaited_once_with(
        "Please choose a history period between 1 and 30 days."
    )


@pytest.mark.asyncio
async def test_history_command_rejects_period_below_one_day():
    """Reject zero or negative periods."""

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    history_command = Mock()
    history_command.handle = AsyncMock()

    current_date_resolver = Mock()

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(
        return_value=TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
        )
    )

    command = DiscordHistorySlashCommand(
        history_command,
        current_date_resolver,
        membership_repository,
    )

    await command.handle(interaction, days=0)

    history_command.handle.assert_not_awaited()
    current_date_resolver.resolve.assert_not_called()

    interaction.response.send_message.assert_awaited_once_with(
        "Please choose a history period between 1 and 30 days."
    )


@pytest.mark.asyncio
async def test_history_command_requires_tracker_membership():
    """Prompt users to join before viewing their history."""

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    history_command = Mock()
    history_command.handle = AsyncMock()

    current_date_resolver = Mock()

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(return_value=None)

    command = DiscordHistorySlashCommand(
        history_command,
        current_date_resolver,
        membership_repository,
    )

    await command.handle(interaction)

    history_command.handle.assert_not_awaited()
    current_date_resolver.resolve.assert_not_called()

    interaction.response.send_message.assert_awaited_once_with(
        "You're not participating in the tracker. Use `/streak join` first."
    )
