from datetime import datetime, timezone

from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.repositories.message_repository import MessageRepository


async def test_repository_records_message():

    # Arrange
    repository = MessageRepository()
    event = MessageEvent(
        user_id=12345,
        timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
    )

    # Act
    await repository.record(event)
    result = await repository.has_message_for_date(
        event.user_id,
        event.timestamp.date(),
    )

    # Assert
    assert result is True

async def test_repository_returns_false_when_no_message_exists():

    # Arrange
    repository = MessageRepository()
    event = MessageEvent(
        user_id=12345,
        timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
    )

    # Act
    result = await repository.has_message_for_date(
        event.user_id,
        event.timestamp.date(),
    )

    # Assert
    assert result is False
