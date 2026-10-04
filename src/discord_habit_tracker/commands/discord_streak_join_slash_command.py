import discord

from discord_habit_tracker.commands.timezone_select_view import (
    TimezoneSelectView,
)


class DiscordStreakJoinSlashCommand:
    """Discord adapter for the /streak join command."""

    def __init__(self, membership_service):
        self._membership_service = membership_service

    async def handle(self, interaction: discord.Interaction):
        """Present the timezone selector."""

        view = TimezoneSelectView(self._membership_service)

        await interaction.response.send_message(
            "Select your timezone to join the tracker.",
            view=view,
        )
