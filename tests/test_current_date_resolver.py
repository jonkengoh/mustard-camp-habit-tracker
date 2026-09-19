from datetime import date, datetime, timezone

from discord_habit_tracker.services.current_date_resolver import (
    CurrentDateResolver,
)


def test_current_date_resolver_returns_date_in_configured_timezone(monkeypatch):
    """Test that the resolver returns today's date in the configured timezone."""

    known_timestamp = datetime(
        2026,
        9,
        20,
        16,
        30,
        tzinfo=timezone.utc,
    )

    class MockDateTime:
        @classmethod
        def now(cls, tz):
            return known_timestamp.astimezone(tz)

    monkeypatch.setattr(
        "discord_habit_tracker.services.current_date_resolver.datetime",
        MockDateTime,
    )

    resolver = CurrentDateResolver()

    result = resolver.resolve("Asia/Singapore")

    assert result == date(2026, 9, 21)
