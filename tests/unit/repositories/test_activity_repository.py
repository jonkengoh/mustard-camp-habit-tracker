from datetime import date
from discord_habit_tracker.models.activity_event import ActivityEvent
from discord_habit_tracker.repositories.activity_repository import ActivityRepository


async def test_records_activity():
    repository = ActivityRepository()

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 15),
    )

    await repository.record(activity)

    result = await repository.has_activity_for_date(
        999,
        12345,
        date(2026, 9, 15),
    )

    assert result is True


async def test_returns_false_when_activity_does_not_exist():
    repository = ActivityRepository()

    result = await repository.has_activity_for_date(
        999,
        12345,
        date(2026, 9, 15),
    )

    assert result is False


async def test_different_dates_are_tracked_separately():
    repository = ActivityRepository()

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 15),
    )

    await repository.record(activity)

    result = await repository.has_activity_for_date(
        999,
        12345,
        date(2026, 9, 16),
    )

    assert result is False


async def test_different_users_are_tracked_separately():
    repository = ActivityRepository()

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 9, 15),
    )

    await repository.record(activity)

    result = await repository.has_activity_for_date(
        999,
        67890,
        date(2026, 9, 15),
    )

    assert result is False



async def test_activity_dates_can_be_retrieved_for_user():
    """Test that all recorded activity dates can be retrieved for a user."""

    repository = ActivityRepository()

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


async def test_different_guilds_are_tracked_separately():
    """Test that activity in different guilds is tracked independently."""

    repository = ActivityRepository()

    activity_date = date(2026, 8, 31)

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


async def test_activity_dates_can_be_retrieved_within_date_range():
    """Return only activity dates within the inclusive date range."""

    repository = ActivityRepository()

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


async def test_activity_date_range_does_not_include_other_users_or_guilds():
    """Return only dates belonging to the specified user and guild."""

    repository = ActivityRepository()

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


async def test_activity_date_range_returns_empty_set_when_no_activity_matches():
    """Return an empty set when no dates fall within the range."""

    repository = ActivityRepository()

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


async def test_activity_date_range_returns_empty_set_when_start_is_after_end():
    """Return an empty set for an invalid date range."""

    repository = ActivityRepository()

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
