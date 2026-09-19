class DiscordStreakSlashCommand:
    """Handles the Discord slash command for streaks."""

    def __init__(self, streak_command):
        self._streak_command = streak_command

    async def handle(self, interaction, current_date):
        """Handle the Discord interaction."""

        response = await self._streak_command.handle(
            interaction.user.id,
            current_date,
        )

        await interaction.response.send_message(response)
