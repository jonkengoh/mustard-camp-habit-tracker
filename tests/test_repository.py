from datetime import date

from discord_habit_tracker.models.activity_event import ActivityEvent
from discord_habit_tracker.repositories.activity_repository import ActivityRepository


async def test_repository_records_activity():

    # Arrange
    repository = ActivityRepository()
    event = ActivityEvent(
        user_id=12345,
        activity_date=date(2026, 8, 31),
    )

    # Act
    await repository.record(event)
    result = await repository.has_activity_for_date(
        event.user_id,
        event.activity_date,
    )

    # Assert
    assert result is True


async def test_repository_returns_false_when_no_activity_exists():

    # Arrange
    repository = ActivityRepository()

    # Act
    result = await repository.has_activity_for_date(
        12345,
        date(2026, 8, 31),
    )

    # Assert
    assert result is False


async def test_repository_does_not_confuse_different_dates():

    # Arrange
    repository = ActivityRepository()
    event = ActivityEvent(
        user_id=12345,
        activity_date=date(2026, 8, 31),
    )

    # Act
    await repository.record(event)
    result = await repository.has_activity_for_date(
        event.user_id,
        date(2026, 9, 1),
    )

    # Assert
    assert result is False


async def test_repository_does_not_confuse_different_users():

    # Arrange
    repository = ActivityRepository()
    event = ActivityEvent(
        user_id=12345,
        activity_date=date(2026, 8, 31),
    )

    # Act
    await repository.record(event)
    result = await repository.has_activity_for_date(
        67890,
        date(2026, 8, 31),
    )

    # Assert
    assert result is False
