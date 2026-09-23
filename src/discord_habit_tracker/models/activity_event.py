from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ActivityEvent:
    """Represents a user's activity for a calendar date."""

    guild_id: int
    user_id: int
    activity_date: date
