import discord
from unittest.mock import Mock

from discord_habit_tracker.commands.discord_timezone_select import (
    TimezoneSelect,
)


def test_timezone_select_contains_curated_timezone_options():
    select = TimezoneSelect(Mock())

    assert len(select.options) == 24

    singapore = select.options[0]

    assert singapore.label == "🇸🇬 Singapore (UTC+08:00)"
    assert singapore.value == "Asia/Singapore"
