from datetime import datetime, timezone

from discord_habit_tracker.services.activity_date_resolver import (
    ActivityDateResolver,
)


def test_resolves_date_in_singapore_timezone():
    """Test that a UTC timestamp is converted to Singapore local date."""

    resolver = ActivityDateResolver()

    timestamp = datetime(
        2026,
        9,
        17,
        4,
        30,
        tzinfo=timezone.utc,
    )

    result = resolver.resolve(
        timestamp,
        "Asia/Singapore",
    )

    assert result.isoformat() == "2026-09-17"


def test_resolves_date_in_st_louis_timezone():
    """Test that a UTC timestamp is converted to St. Louis local date."""

    resolver = ActivityDateResolver()

    timestamp = datetime(
        2026,
        9,
        17,
        4,
        30,
        tzinfo=timezone.utc,
    )

    result = resolver.resolve(
        timestamp,
        "America/Chicago",
    )

    assert result.isoformat() == "2026-09-16"
