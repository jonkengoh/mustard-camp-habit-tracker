from datetime import datetime, timezone

from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.repositories.activity_repository import ActivityRepository
from discord_habit_tracker.services.activity_qualification_service import (
    ActivityQualificationService,
)
from discord_habit_tracker.services.activity_date_resolver import (
    ActivityDateResolver,
)


async def test_first_message_is_recorded():
    """Test that the first message from the tracked user is recorded."""

    # Arrange
    repository = ActivityRepository()
    qualification_service = ActivityQualificationService()
    date_resolver = ActivityDateResolver()

    listener = EventListener(
        repository,
        tracked_user_ids={12345},
        activity_qualification_service=qualification_service,
        activity_date_resolver=date_resolver,
        tracked_user_timezone="Asia/Singapore",
    )

    event = MessageEvent(
        user_id=12345,
        timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
    )

    # Act
    await listener.handle_message(event)

    # Assert
    result = await repository.has_activity_for_date(
        event.user_id,
        event.timestamp.date(),
    )

    assert result is True
