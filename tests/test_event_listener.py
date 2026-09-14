
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

    mock_repository.has_message_for_date.return_value = False # Simulate that the user does not have a message for that date

    tracked_user_id=12345

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_id,
        mock_qualification_service,
    )

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

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_id,
        mock_qualification_service,
    )

    await listener.handle_message(event)

    mock_repository.record.assert_not_awaited()  # Ensure that the record method was not called for a non-tracked user


async def test_event_listener_checks_if_user_has_existing_message():
    """When a tracked user sends a message, the EventListener should ask the repository whether that user already has a message recorded for that date."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    tracked_user_id=12345

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_id,
        mock_qualification_service,
    )

    await listener.handle_message(event)


    mock_repository.has_message_for_date.assert_awaited_once_with(
        event.user_id,
        event.timestamp.date()
    )


async def test_event_listener_ignores_if_user_has_existing_message():
    """When a tracked user has already sent a message on that date, the EventListener should not record the new event."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    mock_repository.has_message_for_date.return_value = True  # Simulate that the user already has a message for that date

    tracked_user_id=12345

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_id,
        mock_qualification_service,
    )

    await listener.handle_message(event)

    mock_repository.record.assert_not_awaited()  # Ensure that the record method was not called for a user who already has a message recorded for that date

async def test_event_listener_checks_activity_qualification():
    """The EventListener should ask whether a tracked message qualifies as activity."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()
    mock_repository.has_message_for_date.return_value = False

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    tracked_user_id = 12345

    listener = EventListener(
        mock_repository,
        tracked_user_id,
        mock_qualification_service,
    )

    await listener.handle_message(event)

    mock_qualification_service.qualifies.assert_awaited_once_with(event)


async def test_event_listener_ignores_non_qualifying_activity():
    """The EventListener should not record a message that does not qualify as activity."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()
    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = False

    tracked_user_id = 12345

    listener = EventListener(
        mock_repository,
        tracked_user_id,
        mock_qualification_service,
    )

    await listener.handle_message(event)

    # Ensure that the qualifies method was called with the event
    mock_qualification_service.qualifies.assert_awaited_once_with(event)
    # Ensure that the repository methods were not called since the activity did not qualify
    mock_repository.has_message_for_date.assert_not_awaited()
    mock_repository.record.assert_not_awaited()
