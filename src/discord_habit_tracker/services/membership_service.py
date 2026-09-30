from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from discord_habit_tracker.services.exceptions import InvalidTimezoneError, MemberAlreadyExistsError, MemberNotFoundError

class MembershipService:
    """Manages tracker membership."""

    def __init__(self, membership_repository):
        self._membership_repository = membership_repository

    async def join(
        self,
        guild_id: int,
        user_id: int,
        timezone: str,
    ):
        """Add a user to the tracker."""

        existing_member = await self._membership_repository.get_member(
            guild_id,
            user_id,
        )

        if existing_member is not None:
            raise MemberAlreadyExistsError

        try:
            ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            raise InvalidTimezoneError

        await self._membership_repository.add_member(
            guild_id,
            user_id,
            timezone,
        )

    async def leave(
        self,
        guild_id: int,
        user_id: int,
    ):
        """Remove a user from the tracker."""

        existing_member = await self._membership_repository.get_member(
            guild_id,
            user_id,
        )

        if existing_member is None:
            raise MemberNotFoundError

        await self._membership_repository.remove_member(
            guild_id,
            user_id,
        )
