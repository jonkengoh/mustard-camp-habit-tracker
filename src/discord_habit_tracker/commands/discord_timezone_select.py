from datetime import datetime, timezone

import discord

from discord_habit_tracker.timezones import (
    TIMEZONE_OPTIONS,
    format_timezone_label,
)


class TimezoneSelect(discord.ui.Select):
    """Discord timezone selection menu."""

    def __init__(self, membership_service):
        self._membership_service = membership_service

        reference_datetime = datetime.now(timezone.utc)

        options = [
            discord.SelectOption(
                label=format_timezone_label(
                    option,
                    reference_datetime,
                ),
                value=option.timezone,
            )
            for option in TIMEZONE_OPTIONS
        ]

        super().__init__(
            placeholder="Select your timezone",
            options=options,
        )
