class MembershipRepository:
    """Stores tracker membership."""

    def __init__(self):
        self._members = set()

    async def add_member(
        self,
        guild_id: int,
        user_id: int,
    ):
        """Add a user to a guild's tracker."""

        self._members.add((guild_id, user_id))

    async def is_member(
        self,
        guild_id: int,
        user_id: int,
    ) -> bool:
        """Return whether a user is a member of a guild's tracker."""

        return (guild_id, user_id) in self._members

    async def remove_member(
        self,
        guild_id: int,
        user_id: int,
    ):
        """Remove a user from a guild's tracker."""

        self._members.discard((guild_id, user_id))
