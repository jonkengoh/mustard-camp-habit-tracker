from datetime import datetime, timezone

import discord

from discord_habit_tracker.timezones import (
        TIMEZONE_OPTIONS,
        format_timezone_label,
    )
from discord_habit_tracker.services.exceptions import (
        InvalidTimezoneError,
        MemberNotFoundError,
    )

class TimezoneUpdateSelect(discord.ui.Select):
    """Discord timezone selection menu for existing members."""

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
            placeholder="Select your new timezone",
            options=options,
        )
    async def callback(self, interaction: discord.Interaction):
        """Handle a selected timezone update."""
        selected_timezone = self.values[0]
        try:
            await self._membership_service.update_timezone(
                interaction.guild.id,
                interaction.user.id,
                selected_timezone,
            )
        except MemberNotFoundError:
            await interaction.response.send_message(
                "You're not participating in the tracker. Use /streak join first."
            )
            return
        except InvalidTimezoneError:
            await interaction.response.send_message(
                "The selected timezone is invalid."
            )
            return
        self.disabled = True
        selected_option = next(
            option
            for option in TIMEZONE_OPTIONS
            if option.timezone == selected_timezone
        )
        await interaction.response.send_message(
            f"Your timezone has been updated to {selected_option.name}."
        )
