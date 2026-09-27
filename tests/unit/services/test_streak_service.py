from datetime import date

from discord_habit_tracker.services.streak_service import StreakService


def test_current_streak_counts_consecutive_activity_dates():
    """Test that the current streak counts consecutive activity dates."""

    service = StreakService()

    activity_dates = {
        date(2026, 9, 16),
        date(2026, 9, 17),
        date(2026, 9, 18),
    }

    result = service.calculate_current_streak(
        activity_dates,
        date(2026, 9, 18),
    )

    assert result == 3


def test_current_streak_stops_at_missing_activity_date():
    """Test that the current streak stops when a day is missing."""

    service = StreakService()

    activity_dates = {
        date(2026, 9, 14),
        date(2026, 9, 15),
        date(2026, 9, 17),
        date(2026, 9, 18),
    }

    result = service.calculate_current_streak(
        activity_dates,
        date(2026, 9, 18),
    )

    assert result == 2


def test_current_streak_is_zero_when_there_is_no_activity_today():
    """Test that the current streak is zero when today has no activity."""

    service = StreakService()

    activity_dates = {
        date(2026, 9, 15),
        date(2026, 9, 16),
        date(2026, 9, 17),
    }

    result = service.calculate_current_streak(
        activity_dates,
        date(2026, 9, 18),
    )

    assert result == 0


def test_current_streak_is_zero_when_there_is_no_activity():
    """Test that the current streak is zero when there is no activity."""

    service = StreakService()

    result = service.calculate_current_streak(
        set(),
        date(2026, 9, 18),
    )

    assert result == 0


def test_longest_streak_counts_consecutive_activity_dates():
    """Test that the longest streak counts the longest consecutive run."""

    service = StreakService()

    activity_dates = {
        date(2026, 9, 16),
        date(2026, 9, 17),
        date(2026, 9, 18),
    }

    result = service.calculate_longest_streak(activity_dates)

    assert result == 3


def test_longest_streak_returns_longest_of_multiple_streaks():
    """Test that the longest streak is selected from multiple streaks."""

    service = StreakService()

    activity_dates = {
        date(2026, 9, 10),
        date(2026, 9, 11),
        date(2026, 9, 13),
        date(2026, 9, 14),
        date(2026, 9, 15),
        date(2026, 9, 17),
    }

    result = service.calculate_longest_streak(activity_dates)

    assert result == 3


def test_longest_streak_is_zero_when_there_is_no_activity():
    """Test that the longest streak is zero when there is no activity."""

    service = StreakService()

    result = service.calculate_longest_streak(set())

    assert result == 0
