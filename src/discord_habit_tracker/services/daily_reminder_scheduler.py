from datetime import time
from zoneinfo import ZoneInfo
class DailyReminderScheduler:
    """Coordinates scheduled daily streak reminders."""
    def __init__(
        self,
        membership_repository,
        eligibility_service,
        notifier,
        delivery_repository,
        discord_client,
        activity_stats_service,
        clock,
        reminder_time_resolver=None,
        delivery_window_seconds: int = 60,
    ):
        self._membership_repository = membership_repository
        self._eligibility_service = eligibility_service
        self._notifier = notifier
        self._delivery_repository = delivery_repository
        self._discord_client = discord_client
        self._activity_stats_service = activity_stats_service
        self._clock = clock
        self._reminder_time_resolver = (
            reminder_time_resolver or DefaultReminderTimeResolver()
        )
        self._delivery_window_seconds = delivery_window_seconds
    async def check_reminders(self) -> None:
        """Send reminders to eligible members whose scheduled time is due."""
        members = (
            await self._membership_repository.get_members_with_reminders_enabled()
        )
        for member in members:
            now = self._clock.now().astimezone(ZoneInfo(member.timezone))
            reminder_time = self._reminder_time_resolver.resolve(member)
            if not self._is_within_delivery_window(now, reminder_time):
                continue
            if not await self._eligibility_service.is_eligible(
                member.guild_id,
                member.user_id,
            ):
                continue
            guild = self._discord_client.get_guild(member.guild_id)
            if guild is None:
                continue
            current_streak = (
                await self._activity_stats_service.get_current_streak(
                    member.guild_id,
                    member.user_id,
                    now.date(),
                )
            )
            await self._notifier.notify_reminder(
                guild,
                user_id=member.user_id,
                current_streak=current_streak,
            )
            await self._delivery_repository.record_delivery(
                member.guild_id,
                member.user_id,
                now.date().isoformat(),
            )
    def _is_within_delivery_window(self, now, reminder_time) -> bool:
        """Return whether the local time is within the reminder delivery window."""

        scheduled_at = now.replace(
            hour=reminder_time.hour,
            minute=reminder_time.minute,
            second=0,
            microsecond=0,
        )

        elapsed_seconds = (now - scheduled_at).total_seconds()

        return 0 <= elapsed_seconds < self._delivery_window_seconds


class DefaultReminderTimeResolver:
    """Resolves the default daily reminder time."""
    def resolve(self, member) -> time:
        """Return the default reminder time of 9 PM."""
        return time(21, 0)
