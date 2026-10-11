from datetime import date

from discord_habit_tracker.models.activity_event import ActivityEvent


def test_activity_event_stores_user_and_date():
    """Test that an ActivityEvent stores the user and activity date."""

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 15),
    )

    assert activity.user_id == 12345
    assert activity.activity_date == date(2026, 9, 15)
