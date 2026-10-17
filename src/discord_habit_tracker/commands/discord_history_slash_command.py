from datetime import timedelta


class DiscordHistorySlashCommand:
    """Handles the Discord history slash command."""

    def __init__(
        self,
        history_command,
        current_date_resolver,
        membership_repository,
    ):
        self._history_command = history_command
        self._current_date_resolver = current_date_resolver
        self._membership_repository = membership_repository

    async def handle(self, interaction, days: int = 7):
        """Handle a history request for the specified number of days."""

        if not 1 <= days <= 30:
            await interaction.response.send_message(
                "Please choose a history period between 1 and 30 days."
            )
            return

        member = await self._membership_repository.get_member(
            interaction.guild.id,
            interaction.user.id,
        )

        if member is None:
            await interaction.response.send_message(
                "You're not participating in the tracker. "
                "Use `/streak join` first."
            )
            return

        current_date = self._current_date_resolver.resolve(member.timezone)
        start_date = current_date - timedelta(days=days - 1)

        response = await self._history_command.handle(
            interaction.guild.id,
            interaction.user.id,
            start_date,
            current_date,
        )

        await interaction.response.send_message(response)
