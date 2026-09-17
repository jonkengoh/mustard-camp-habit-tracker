from datetime import date

import pytest

from discord_habit_tracker.models.activity_event import ActivityEvent
from discord_habit_tracker.repositories.sqlite_activity_repository import (
    SQLiteActivityRepository,
)


@pytest.mark.asyncio
async def test_recorded_activity_can_be_found():
    """Test that a recorded activity can be retrieved by date."""

    repository = SQLiteActivityRepository(":memory:")

    activity = ActivityEvent(
        user_id=12345,
        activity_date=date(2026, 9, 16),
    )

    await repository.record(activity)

    result = await repository.has_activity_for_date(
        12345,
        date(2026, 9, 16),
    )

    assert result is True


@pytest.mark.asyncio
async def test_missing_activity_cannot_be_found():
    """Test that an unrecorded activity is not found."""

    repository = SQLiteActivityRepository(":memory:")

    result = await repository.has_activity_for_date(
        12345,
        date(2026, 9, 16),
    )

    assert result is False


@pytest.mark.asyncio
async def test_recording_duplicate_activity_does_not_fail():
    """Test that recording the same activity twice is safe."""

    repository = SQLiteActivityRepository(":memory:")

    activity = ActivityEvent(
        user_id=12345,
        activity_date=date(2026, 9, 16),
    )

    await repository.record(activity)
    await repository.record(activity)

    result = await repository.has_activity_for_date(
        12345,
        date(2026, 9, 16),
    )

    assert result is True


@pytest.mark.asyncio
async def test_recorded_activity_persists_across_repository_instances(tmp_path):
    """Test that recorded activity persists across repository instances."""

    database_path = tmp_path / "activity_tracker.db"

    first_repository = SQLiteActivityRepository(str(database_path))

    activity = ActivityEvent(
        user_id=12345,
        activity_date=date(2026, 9, 16),
    )

    await first_repository.record(activity)

    second_repository = SQLiteActivityRepository(str(database_path))

    result = await second_repository.has_activity_for_date(
        12345,
        date(2026, 9, 16),
    )

    assert result is True


def test_repository_can_be_closed(tmp_path):
    """Test that the repository closes its database connection."""

    database_path = tmp_path / "activity_tracker.db"

    repository = SQLiteActivityRepository(str(database_path))

    repository.close()

    assert repository._connection is None
