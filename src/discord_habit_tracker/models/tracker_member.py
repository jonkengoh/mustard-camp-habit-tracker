from dataclasses import dataclass


@dataclass(frozen=True)
class TrackerMember:
    """Represents a user's membership in a guild's activity tracker."""

    guild_id: int
    user_id: int
    timezone: str
