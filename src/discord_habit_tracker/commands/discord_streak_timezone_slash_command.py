import discord

from discord_habit_tracker.commands.timezone_update_select_view import (
TimezoneUpdateSelectView,
)

class DiscordStreakTimezoneSlashCommand:
    """Discord adapter for the /streak timezone command."""

    def __init__(self, membership_service):
        self._membership_service = membership_service

    async def handle(self, interaction: discord.Interaction):
        """Present the timezone update selector."""
        view = TimezoneUpdateSelectView(self._membership_service)
        await interaction.response.send_message(
            "Select your new timezone.",
            view=view,
        )
