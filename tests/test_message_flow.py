from datetime import datetime, timezone

from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.repositories.message_repository import MessageRepository
from discord_habit_tracker.services.activity_qualification_service import (
    ActivityQualificationService,
)


async def test_first_message_is_recorded():
    """Test that the first message from the tracked user is recorded."""

    # Arrange
    repository = MessageRepository()
    qualification_service = ActivityQualificationService()

    listener = EventListener(
        repository,
        tracked_user_id=12345,
        activity_qualification_service=qualification_service
    )

    event = MessageEvent(
        user_id=12345,
        timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
    )

    # Act
    await listener.handle_message(event)

    # Assert
    result = await repository.has_message_for_date(
        event.user_id,
        event.timestamp.date(),
    )

    assert result is True
