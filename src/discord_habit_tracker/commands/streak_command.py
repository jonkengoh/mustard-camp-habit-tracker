from datetime import date

class StreakCommand:
    """Handles the streak command."""

    def __init__(self, activity_stats_service):
        self._activity_stats_service = activity_stats_service

    async def handle(
        self,
        user_id: int,
        current_date: date,
    ) -> str:
        """Return the user's current and longest streaks."""

        current_streak = (
            await self._activity_stats_service.get_current_streak(
                user_id,
                current_date,
            )
        )

        longest_streak = (
            await self._activity_stats_service.get_longest_streak(
                user_id,
            )
        )

        return (
            f"Current streak: {current_streak} days\n"
            f"Longest streak: {longest_streak} days"
        )
