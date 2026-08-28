from datetime import datetime

from discord_habit_tracker.models.message_event import MessageEvent


def test_message_event_stores_message_data():
    """Test that MessageEvent stores the user ID and timestamp."""

    timestamp = datetime(2026, 8, 28, 14, 5)

    event = MessageEvent(
        user_id=123456789,
        timestamp=timestamp,
    )

    assert event.user_id == 123456789
    assert event.timestamp == timestamp
