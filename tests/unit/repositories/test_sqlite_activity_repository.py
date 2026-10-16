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

    cursor = repository._connection.execute(
        """
        SELECT COUNT(*)
        FROM activities
        WHERE guild_id = ? AND user_id = ? AND activity_date = ?
        """,
        (
            activity.guild_id,
            activity.user_id,
            activity.activity_date.isoformat(),
        ),
    )

    assert cursor.fetchone()[0] == 1


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


@pytest.mark.asyncio
async def test_activity_dates_can_be_retrieved_within_date_range():
    """Return only activity dates within the inclusive date range."""

    repository = SQLiteActivityRepository(":memory:")

    for activity_date in (
        date(2026, 10, 1),
        date(2026, 10, 3),
        date(2026, 10, 5),
        date(2026, 10, 8),
    ):
        await repository.record(
            ActivityEvent(
                guild_id=999,
                user_id=12345,
                activity_date=activity_date,
            )
        )

    result = await repository.get_activity_dates_in_range(
        999,
        12345,
        date(2026, 10, 3),
        date(2026, 10, 5),
    )

    assert result == {
        date(2026, 10, 3),
        date(2026, 10, 5),
    }


@pytest.mark.asyncio
async def test_activity_date_range_does_not_include_other_users_or_guilds():
    """Return only dates belonging to the specified user and guild."""

    repository = SQLiteActivityRepository(":memory:")

    activity_date = date(2026, 10, 3)

    for guild_id, user_id in (
        (999, 12345),
        (999, 67890),
        (1000, 12345),
    ):
        await repository.record(
            ActivityEvent(
                guild_id=guild_id,
                user_id=user_id,
                activity_date=activity_date,
            )
        )

    result = await repository.get_activity_dates_in_range(
        999,
        12345,
        date(2026, 10, 1),
        date(2026, 10, 5),
    )

    assert result == {activity_date}


@pytest.mark.asyncio
async def test_activity_date_range_returns_empty_set_when_no_activity_matches():
    """Return an empty set when no dates fall within the range."""

    repository = SQLiteActivityRepository(":memory:")

    await repository.record(
        ActivityEvent(
            guild_id=999,
            user_id=12345,
            activity_date=date(2026, 10, 1),
        )
    )

    result = await repository.get_activity_dates_in_range(
        999,
        12345,
        date(2026, 10, 3),
        date(2026, 10, 5),
    )

    assert result == set()


@pytest.mark.asyncio
async def test_activity_date_range_returns_empty_set_when_start_is_after_end():
    """Return an empty set for an invalid date range."""

    repository = SQLiteActivityRepository(":memory:")

    await repository.record(
        ActivityEvent(
            guild_id=999,
            user_id=12345,
            activity_date=date(2026, 10, 3),
        )
    )

    result = await repository.get_activity_dates_in_range(
        999,
        12345,
        date(2026, 10, 5),
        date(2026, 10, 1),
    )

    assert result == set()
