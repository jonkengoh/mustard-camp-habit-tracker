class DiscordStreakSlashCommand:
    """Handles the Discord slash command for streaks."""

    def __init__(
        self,
        streak_command,
        current_date_resolver,
        membership_repository,
    ):
        self._streak_command = streak_command
        self._current_date_resolver = current_date_resolver
        self._membership_repository = membership_repository

    async def handle(self, interaction):
        member = await self._membership_repository.get_member(
            interaction.guild.id,
            interaction.user.id,
        )

        if member is None:
            await interaction.response.send_message(
                "You're not participating in the tracker. Use `/streak join` first."
            )
            return

        current_date = self._current_date_resolver.resolve(
            member.timezone,
        )

        response = await self._streak_command.handle(
            interaction.guild.id,
            interaction.user.id,
            current_date,
        )


        await interaction.response.send_message(response)
