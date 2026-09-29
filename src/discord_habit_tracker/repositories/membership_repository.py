from discord_habit_tracker.models.tracker_member import TrackerMember


class MembershipRepository:
    """Stores tracker membership."""

    def __init__(self):
        self._members = {}

    async def add_member(
        self,
        guild_id: int,
        user_id: int,
        timezone: str,
    ):
        """Add a user to a guild's tracker."""

        self._members[(guild_id, user_id)] = TrackerMember(
            guild_id=guild_id,
            user_id=user_id,
            timezone=timezone,
        )

    async def get_member(
        self,
        guild_id: int,
        user_id: int,
    ) -> TrackerMember | None:
        """Return a guild tracker member, if one exists."""

        return self._members.get((guild_id, user_id))

    async def remove_member(
        self,
        guild_id: int,
        user_id: int,
    ):
        """Remove a user from a guild's tracker."""

        self._members.pop((guild_id, user_id), None)
