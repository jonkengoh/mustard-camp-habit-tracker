from datetime import date, datetime
from zoneinfo import ZoneInfo


class ActivityDateResolver:
    """Resolves a timestamp to a local calendar date."""

    def resolve(self, timestamp: datetime, timezone_name: str) -> date:
        """Return the calendar date for a timestamp in the given timezone."""

        local_timestamp = timestamp.astimezone(ZoneInfo(timezone_name))

        return local_timestamp.date()
