class ReminderEligibilityService:
    """Determines whether a tracker member should receive a daily reminder."""

    def __init__(
        self,
        membership_repository,
        current_date_resolver,
        activity_repository,
        activity_stats_service,
        delivery_repository,
    ):
        self._membership_repository = membership_repository
        self._current_date_resolver = current_date_resolver
        self._activity_repository = activity_repository
        self._activity_stats_service = activity_stats_service
        self._delivery_repository = delivery_repository

    async def is_eligible(
        self,
        guild_id: int,
        user_id: int,
    ) -> bool:
        """Return whether a member should receive a reminder today."""

        member = await self._membership_repository.get_member(
            guild_id,
            user_id,
        )

        if member is None or not member.reminders_enabled:
            return False

        current_date = self._current_date_resolver.resolve(
            member.timezone,
        )

        has_activity_today = (
            await self._activity_repository.has_activity_for_date(
                guild_id,
                user_id,
                current_date,
            )
        )

        if has_activity_today:
            return False

        current_streak = (
            await self._activity_stats_service.get_current_streak(
                guild_id,
                user_id,
                current_date,
            )
        )

        if current_streak <= 0:
            return False

        reminder_date = current_date.isoformat()

        already_reminded = (
            await self._delivery_repository.has_delivery(
                guild_id,
                user_id,
                reminder_date,
            )
        )

        if already_reminded:
            return False

        return True
