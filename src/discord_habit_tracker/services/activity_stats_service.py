from datetime import date, timedelta


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


    async def get_recent_activity_stats(
        self,
        guild_id: int,
        user_id: int,
        current_date: date,
    ) -> dict:
        """Return activity statistics for the last 30 calendar days."""

        start_date = current_date - timedelta(days=29)

        activity_dates = (
            await self._activity_repository.get_activity_dates_in_range(
                guild_id,
                user_id,
                start_date,
                current_date,
            )
        )

        total_days = 30
        active_days = len(activity_dates)
        activity_rate = active_days / total_days * 100

        return {
            "active_days": active_days,
            "total_days": total_days,
            "activity_rate": activity_rate,
        }
