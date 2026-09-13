from discord_habit_tracker.models.message_event import MessageEvent


class ActivityQualificationService:
    """Determines whether a MessageEvent qualifies as activity."""

    async def qualifies(self, event: MessageEvent) -> bool:
        """Return whether the event qualifies as activity."""

        return True
