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
        12345,
        date(2026, 9, 15),
    )

    assert result is True


async def test_returns_false_when_activity_does_not_exist():
    repository = ActivityRepository()

    result = await repository.has_activity_for_date(
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

    result = await repository.get_activity_dates(12345)

    assert result == {
        date(2026, 9, 16),
        date(2026, 9, 17),
    }
