import discord

from discord_habit_tracker.services.exceptions import MemberNotFoundError


class DiscordStreakLeaveSlashCommand:
    """Discord adapter for the /streak leave command."""

    def __init__(self, membership_service):
        self._membership_service = membership_service

    async def handle(self, interaction: discord.Interaction):
        """Remove the user from the tracker."""

        try:
            await self._membership_service.leave(
                interaction.guild.id,
                interaction.user.id,
            )
        except MemberNotFoundError:
            await interaction.response.send_message(
                "You're not participating in the tracker."
            )
            return

        await interaction.response.send_message(
            "You've left the activity tracker."
        )
