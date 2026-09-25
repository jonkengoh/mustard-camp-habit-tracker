from datetime import date

import pytest
import sqlite3

from discord_habit_tracker.models.activity_event import ActivityEvent
from discord_habit_tracker.repositories.sqlite_activity_repository import (
    SQLiteActivityRepository,
)


@pytest.mark.asyncio
async def test_recorded_activity_can_be_found():
    """Test that a recorded activity can be retrieved by date."""

    repository = SQLiteActivityRepository(":memory:")

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 16),
    )

    await repository.record(activity)

    result = await repository.has_activity_for_date(
        999,
        12345,
        date(2026, 9, 16),
    )

    assert result is True


@pytest.mark.asyncio
async def test_missing_activity_cannot_be_found():
    """Test that an unrecorded activity is not found."""

    repository = SQLiteActivityRepository(":memory:")

    result = await repository.has_activity_for_date(
        999,
        12345,
        date(2026, 9, 16),
    )

    assert result is False


@pytest.mark.asyncio
async def test_recording_duplicate_activity_does_not_fail():
    """Test that recording the same activity twice is safe."""

    repository = SQLiteActivityRepository(":memory:")

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 16),
    )

    await repository.record(activity)
    await repository.record(activity)

    result = await repository.has_activity_for_date(
        999,
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
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 16),
    )

    await first_repository.record(activity)

    second_repository = SQLiteActivityRepository(str(database_path))

    result = await second_repository.has_activity_for_date(
        999,
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


@pytest.mark.asyncio
async def test_activity_dates_can_be_retrieved_for_user():
    """Test that all recorded activity dates can be retrieved for a user."""

    repository = SQLiteActivityRepository(":memory:")

    await repository.record(
        ActivityEvent(
            guild_id=999,
            user_id=12345,
            activity_date=date(2026, 9, 16),
        )
    )

    await repository.record(
        ActivityEvent(
            guild_id=999,
            user_id=12345,
            activity_date=date(2026, 9, 17),
        )
    )

    result = await repository.get_activity_dates(
        999,
        12345,
    )

    assert result == {
        date(2026, 9, 16),
        date(2026, 9, 17),
    }


@pytest.mark.asyncio
async def test_different_guilds_are_tracked_separately():
    """Test that activity in different guilds is tracked independently."""

    repository = SQLiteActivityRepository(":memory:")

    activity_date = date(2026, 9, 16)

    await repository.record(
        ActivityEvent(
            guild_id=999,
            user_id=12345,
            activity_date=activity_date,
        )
    )

    assert await repository.has_activity_for_date(
        999,
        12345,
        activity_date,
    )

    assert not await repository.has_activity_for_date(
        1000,
        12345,
        activity_date,
    )


@pytest.mark.asyncio
async def test_old_schema_is_replaced_with_current_schema(tmp_path):
    """Test that an old development database is reset to the current schema."""

    database_path = tmp_path / "activity_tracker.db"

    connection = sqlite3.connect(database_path)

    connection.execute(
        """
        CREATE TABLE activities (
            user_id INTEGER NOT NULL,
            activity_date TEXT NOT NULL,
            PRIMARY KEY (user_id, activity_date)
        )
        """
    )

    connection.execute(
        """
        INSERT INTO activities (user_id, activity_date)
        VALUES (?, ?)
        """,
        (
            12345,
            "2026-09-16",
        ),
    )

    connection.commit()
    connection.close()

    repository = SQLiteActivityRepository(str(database_path))

    # The old activity should no longer exist.
    result = await repository.has_activity_for_date(
        999,
        12345,
        date(2026, 9, 16),
    )

    assert result is False
