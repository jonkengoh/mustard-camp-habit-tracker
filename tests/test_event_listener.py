
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.models.activity_event import ActivityEvent


async def test_event_listener_handles_message():
    """Test that the EventListener can handle a MessageEvent."""

    tracked_user_ids = {12345, 67890}

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    mock_date_resolver = Mock()
    mock_date_resolver.resolve.return_value = event.timestamp.date()

    mock_repository.has_activity_for_date.return_value = False

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    expected_activity = ActivityEvent(
        guild_id=event.guild_id,
        user_id=event.user_id,
        activity_date=event.timestamp.date(),
    )

    mock_repository.record.assert_awaited_once_with(expected_activity)


async def test_event_listener_ignores_untracked_user():
    """Test that the EventListener only processes MessageEvents from the tracked user."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    mock_date_resolver = Mock()

    tracked_user_ids = {67890}

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    mock_repository.record.assert_not_awaited()  # Ensure that the record method was not called for a non-tracked user


async def test_event_listener_checks_if_user_has_existing_activity():
    """When a tracked user sends a message, the EventListener should ask the repository whether that user already has an activity recorded for that date."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    mock_date_resolver = Mock()
    mock_date_resolver.resolve.return_value = event.timestamp.date()

    tracked_user_ids = {12345}

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    mock_date_resolver.resolve.assert_called_once_with(
        event.timestamp,
        "Asia/Singapore",
    )

    mock_repository.has_activity_for_date.assert_awaited_once_with(
        event.guild_id,
        event.user_id,
        event.timestamp.date(),
    )



async def test_event_listener_ignores_if_user_has_existing_activity():
    """When a tracked user has already recorded an activity for that date, the EventListener should not record the new event."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    mock_date_resolver = Mock()

    mock_repository.has_activity_for_date.return_value = True  # Simulate that the user already has an activity for that date

    tracked_user_ids = {12345}

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    mock_repository.record.assert_not_awaited()  # Ensure that the record method was not called for a user who already has an activity recorded for that date

async def test_event_listener_checks_activity_qualification():
    """The EventListener should ask whether a tracked message qualifies as activity."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()
    mock_repository.has_activity_for_date.return_value = False

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    mock_date_resolver = Mock()

    tracked_user_ids = {12345}

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    mock_qualification_service.qualifies.assert_awaited_once_with(event)


async def test_event_listener_ignores_non_qualifying_activity():
    """The EventListener should not record activity that does not qualify."""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()
    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = False
    mock_date_resolver = Mock()

    tracked_user_ids = {12345}

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    # Ensure that the qualifies method was called with the event
    mock_qualification_service.qualifies.assert_awaited_once_with(event)

    # Ensure that the repository methods were not called since the activity did not qualify
    mock_repository.has_activity_for_date.assert_not_awaited()
    mock_repository.record.assert_not_awaited()


async def test_event_listener_uses_resolved_activity_date():
    """Test that the EventListener uses the user's local activity date."""

    known_timestamp = datetime(
        2026,
        9,
        17,
        4,
        30,
        tzinfo=timezone.utc,
    )

    event = MessageEvent(
        guild_id=999,
        user_id = 12345,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()
    mock_repository.has_activity_for_date.return_value = False

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    mock_date_resolver = Mock()
    mock_date_resolver.resolve.return_value = date(2026, 9, 16)

    listener = EventListener(
        mock_repository,
        tracked_user_ids = {12345},
        activity_qualification_service=mock_qualification_service,
        activity_date_resolver=mock_date_resolver,
        tracked_user_timezone="America/Chicago",
    )

    await listener.handle_message(event)

    mock_date_resolver.resolve.assert_called_once_with(
        event.timestamp,
        "America/Chicago",
    )

    mock_repository.has_activity_for_date.assert_awaited_once_with(
        event.guild_id,
        event.user_id,
        date(2026, 9, 16),
    )

    mock_repository.record.assert_awaited_once_with(
        ActivityEvent(
            guild_id=event.guild_id,
            user_id=event.user_id,
            activity_date=date(2026, 9, 16),
        )
    )


async def test_event_listener_handles_message_from_another_tracked_user():
    """Test that the EventListener handles messages from multiple tracked users."""

    tracked_user_ids = {12345, 67890}

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    event = MessageEvent(
        guild_id=999,
        user_id=67890,
        timestamp=known_timestamp,
    )

    mock_repository = AsyncMock()

    mock_date_resolver = Mock()
    mock_date_resolver.resolve.return_value = event.timestamp.date()

    mock_repository.has_activity_for_date.return_value = False

    mock_qualification_service = AsyncMock()
    mock_qualification_service.qualifies.return_value = True

    listener = EventListener(
        mock_repository,
        tracked_user_ids,
        mock_qualification_service,
        mock_date_resolver,
        "Asia/Singapore",
    )

    await listener.handle_message(event)

    expected_activity = ActivityEvent(
        guild_id=event.guild_id,
        user_id=event.user_id,
        activity_date=event.timestamp.date(),
    )

    mock_repository.record.assert_awaited_once_with(expected_activity)
