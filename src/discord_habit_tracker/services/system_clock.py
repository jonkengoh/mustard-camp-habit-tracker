from datetime import datetime, timezone


class SystemClock:
    """Provides the current system time as a timezone-aware datetime."""

    def now(self) -> datetime:
        """Return the current time in UTC."""
        return datetime.now(timezone.utc)
