from datetime import datetime, timezone

from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.services.activity_qualification_service import (
    ActivityQualificationService,
)


async def test_message_qualifies_as_activity():
    """Test that a MessageEvent qualifies as activity."""

    # Arrange
    service = ActivityQualificationService()

    event = MessageEvent(
        guild_id=999,
        user_id=12345,
        timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
    )

    # Act
    result = await service.qualifies(event)

    # Assert
    assert result is True
