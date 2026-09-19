class DiscordStreakSlashCommand:
    """Handles the Discord slash command for streaks."""

    def __init__(
        self,
        streak_command,
        current_date_resolver,
        timezone_name,
    ):
        self._streak_command = streak_command
        self._current_date_resolver = current_date_resolver
        self._timezone_name = timezone_name

    async def handle(self, interaction):
        current_date = self._current_date_resolver.resolve(
            self._timezone_name,
        )

        response = await self._streak_command.handle(
            interaction.user.id,
            current_date,
        )

        await interaction.response.send_message(response)
