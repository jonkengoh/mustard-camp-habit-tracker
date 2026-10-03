import discord
from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.commands.discord_timezone_select import (
    TimezoneSelect,
)
from discord_habit_tracker.services.exceptions import (
    InvalidTimezoneError,
    MemberAlreadyExistsError,
)


def test_timezone_select_contains_curated_timezone_options():
    select = TimezoneSelect(Mock())

    assert len(select.options) == 24

    singapore = select.options[0]

    assert singapore.label == "🇸🇬 Singapore (UTC+08:00)"
    assert singapore.value == "Asia/Singapore"


async def test_timezone_select_joins_user_with_selected_timezone():
    membership_service = Mock()
    membership_service.join = AsyncMock()

    select = TimezoneSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Asia/Singapore"]

    await select.callback(interaction)

    membership_service.join.assert_awaited_once_with(
        999,
        12345,
        "Asia/Singapore",
    )


async def test_timezone_select_confirms_successful_join():
    membership_service = Mock()
    membership_service.join = AsyncMock()

    select = TimezoneSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Asia/Singapore"]

    await select.callback(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "You're now participating! Your timezone is set to Singapore."
    )


async def test_timezone_select_rejects_existing_member():
    membership_service = Mock()
    membership_service.join = AsyncMock(
        side_effect=MemberAlreadyExistsError,
    )

    select = TimezoneSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Asia/Singapore"]

    await select.callback(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "You're already participating in the tracker."
    )


async def test_timezone_select_rejects_invalid_timezone():
    membership_service = Mock()
    membership_service.join = AsyncMock(
        side_effect=InvalidTimezoneError,
    )

    select = TimezoneSelect(membership_service)

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    select._values = ["Not/A/Timezone"]

    await select.callback(interaction)

    interaction.response.send_message.assert_awaited_once_with(
        "The selected timezone is invalid."
    )
