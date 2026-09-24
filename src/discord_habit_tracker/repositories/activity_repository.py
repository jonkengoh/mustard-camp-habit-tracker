from datetime import date

from discord_habit_tracker.models.activity_event import ActivityEvent


class ActivityRepository:
    """Stores and retrieves user activity."""

    def __init__(self):
        self._activities = set()


    async def record(self, activity: ActivityEvent):
        """Record a user's activity."""

        self._activities.add(
            (
                activity.guild_id,
                activity.user_id,
                activity.activity_date,
            )
)


    async def has_activity_for_date(
        self,
        guild_id: int,
        user_id: int,
        activity_date: date,
    ) -> bool:
        """Return whether the user has activity recorded for the date."""

        return (guild_id, user_id, activity_date) in self._activities

    async def get_activity_dates(
        self,
        guild_id: int,
        user_id: int,
    ) -> set[date]:
        """Return all recorded activity dates for the user."""

        return {
            activity_date
            for stored_guild_id, stored_user_id, activity_date in self._activities
            if (
                stored_guild_id == guild_id
                and stored_user_id == user_id
            )
        }
