class DiscordActivityNotifier:
    """Sends activity notifications to a Discord guild."""

    CHANNEL_NAME = "daily-streak"

    async def notify(
        self,
        guild,
        user_id: int,
        current_streak: int,
    ) -> None:
        """Send an activity notification to the guild's activity channel."""

        channel, mention = await self._get_channel_and_mention(
            guild,
            user_id,
        )

        await channel.send(
            f"🎉 {mention} completed today's activity! "
            f"Current streak: **{current_streak} days**."
        )

    async def notify_reminder(
        self,
        guild,
        user_id: int,
        current_streak: int,
    ) -> None:
        """Send a reminder to record today's activity."""

        channel, mention = await self._get_channel_and_mention(
            guild,
            user_id,
        )

        await channel.send(
            f"🔥 {mention}, your current streak is **{current_streak} days**! "
            "Record today's activity to keep it going."
        )

    async def _get_channel_and_mention(
        self,
        guild,
        user_id: int,
    ):
        """Return the activity channel and the member's mention."""

        channel = next(
            (
                channel
                for channel in guild.text_channels
                if channel.name == self.CHANNEL_NAME
            ),
            None,
        )

        if channel is None:
            channel = await guild.create_text_channel(self.CHANNEL_NAME)

        member = guild.get_member(user_id)
        mention = member.mention if member is not None else f"<@{user_id}>"

        return channel, mention
