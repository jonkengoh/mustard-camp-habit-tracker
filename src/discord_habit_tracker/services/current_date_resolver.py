from datetime import datetime
from zoneinfo import ZoneInfo


class CurrentDateResolver:
    """Resolves the current date in a configured timezone."""

    def resolve(self, timezone_name: str):
        """Return the current calendar date in the given timezone."""

        current_timestamp = datetime.now(
            ZoneInfo(timezone_name)
        )

        return current_timestamp.date()
