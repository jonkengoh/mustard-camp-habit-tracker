from datetime import date


class ActivityStatsService:
    """Provides activity statistics for a user."""

    def __init__(self, activity_repository, streak_service):
        self._activity_repository = activity_repository
        self._streak_service = streak_service

    async def get_current_streak(
        self,
        guild_id: int,
        user_id: int,
        current_date: date,
    ) -> int:
        """Return the user's current activity streak."""

        activity_dates = (
            await self._activity_repository.get_activity_dates(
                guild_id,
                user_id,
            )
        )

        return self._streak_service.calculate_current_streak(
            activity_dates,
            current_date,
        )

    async def get_longest_streak(
        self,
        guild_id,
        user_id,
    ) -> int:
        """Return the user's longest activity streak."""

        activity_dates = (
            await self._activity_repository.get_activity_dates(
                guild_id,
                user_id,
            )
        )

        return self._streak_service.calculate_longest_streak(
            activity_dates,
        )
