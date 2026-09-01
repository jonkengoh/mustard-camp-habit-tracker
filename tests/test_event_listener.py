
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.models.message_event import MessageEvent


async def test_event_listener_handles_message():
    """Test that the EventListener can handle a MessageEvent."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    tracked_user_id=12345

    listener = EventListener(mock_repository, tracked_user_id)

    await listener.handle_message(event)

    mock_repository.record.assert_awaited_once_with(event)


async def test_event_listener_ignores_untracked_user():
    """Test that the EventListener can handle a MessageEvent and only records events for the tracked user."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    tracked_user_id=67890

    listener = EventListener(mock_repository, tracked_user_id)

    await listener.handle_message(event)

    mock_repository.record.assert_not_awaited()  # Ensure that the record method was not called for a non-tracked user
