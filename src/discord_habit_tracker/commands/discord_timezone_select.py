from datetime import datetime, timezone

import discord

from discord_habit_tracker.timezones import (
    TIMEZONE_OPTIONS,
    format_timezone_label,
)
from discord_habit_tracker.services.exceptions import (
    InvalidTimezoneError,
    MemberAlreadyExistsError,
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


    async def callback(self, interaction: discord.Interaction):
        """Handle a selected timezone."""

        selected_timezone = self.values[0]

        try:
            await self._membership_service.join(
                interaction.guild.id,
                interaction.user.id,
                selected_timezone,
            )
        except MemberAlreadyExistsError:
            await interaction.response.send_message(
                "You're already participating in the tracker."
            )
            return
        except InvalidTimezoneError:
            await interaction.response.send_message(
                "The selected timezone is invalid."
            )
            return

        selected_option = next(
            option
            for option in TIMEZONE_OPTIONS
            if option.timezone == selected_timezone
        )

        await interaction.response.send_message(
            f"You're now participating! Your timezone is set to {selected_option.name}."
        )
