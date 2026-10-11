import discord
from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.commands.discord_timezone_update_select import (
    TimezoneUpdateSelect,
)
from discord_habit_tracker.services.exceptions import (
    InvalidTimezoneError,
    MemberNotFoundError,
)


def test_timezone_update_select_contains_curated_timezone_options():
    select = TimezoneUpdateSelect(Mock())

    assert len(select.options) == 24

    singapore = select.options[0]

    assert singapore.label == "🇸🇬 Singapore (UTC+08:00)"
    assert singapore.value == "Asia/Singapore"


async def test_timezone_update_select_updates_member_timezone():
    membership_service = Mock()
    membership_service.update_timezone = AsyncMock()

    select = TimezoneUpdateSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Asia/Tokyo"]

    await select.callback(interaction)

    membership_service.update_timezone.assert_awaited_once_with(
        999,
        12345,
        "Asia/Tokyo",
    )


async def test_timezone_update_select_confirms_successful_update():
    membership_service = Mock()
    membership_service.update_timezone = AsyncMock()

    select = TimezoneUpdateSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Asia/Tokyo"]

    await select.callback(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "Your timezone has been updated to Tokyo."
    )


async def test_timezone_update_select_rejects_non_member():
    membership_service = Mock()
    membership_service.update_timezone = AsyncMock(
        side_effect=MemberNotFoundError,
    )

    select = TimezoneUpdateSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Asia/Tokyo"]

    await select.callback(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "You're not participating in the tracker. Use /streak join first."
    )
