from datetime import date

from discord_habit_tracker.models.activity_event import ActivityEvent


class ActivityRepository:
    """Stores and retrieves user activity."""

    def __init__(self):
        self._activities = set()


    async def record(self, activity: ActivityEvent):
        """Record a user's activity."""

        self._activities.add(
            (activity.user_id, activity.activity_date)
        )


    async def has_activity_for_date(
        self,
        user_id: int,
        activity_date: date,
    ) -> bool:
        """Return whether the user has activity recorded for the date."""

        return (user_id, activity_date) in self._activities
