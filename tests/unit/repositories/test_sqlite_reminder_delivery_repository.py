import pytest

from discord_habit_tracker.repositories.sqlite_reminder_delivery_repository import (
    SQLiteReminderDeliveryRepository,
)


@pytest.mark.asyncio
async def test_delivery_can_be_recorded():
    """Test that a reminder delivery can be recorded."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    await repository.record_delivery(
        guild_id=999,
        user_id=12345,
        reminder_date="2026-10-22",
    )

    assert await repository.has_delivery(
        guild_id=999,
        user_id=12345,
        reminder_date="2026-10-22",
    ) is True

    repository.close()


@pytest.mark.asyncio
async def test_missing_delivery_returns_false():
    """Test that a delivery that has not been recorded returns false."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    assert await repository.has_delivery(
        guild_id=999,
        user_id=12345,
        reminder_date="2026-10-22",
    ) is False

    repository.close()


@pytest.mark.asyncio
async def test_delivery_can_be_recorded_for_another_date():
    """Test that a member can receive reminders on different dates."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    await repository.record_delivery(999, 12345, "2026-10-22")
    await repository.record_delivery(999, 12345, "2026-10-23")

    assert await repository.has_delivery(999, 12345, "2026-10-22") is True
    assert await repository.has_delivery(999, 12345, "2026-10-23") is True

    repository.close()


@pytest.mark.asyncio
async def test_deliveries_are_separated_by_guild():
    """Test that deliveries in different guilds are tracked separately."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    await repository.record_delivery(999, 12345, "2026-10-22")

    assert await repository.has_delivery(999, 12345, "2026-10-22") is True
    assert await repository.has_delivery(1000, 12345, "2026-10-22") is False

    repository.close()


@pytest.mark.asyncio
async def test_deliveries_are_separated_by_member():
    """Test that deliveries for different members are tracked separately."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    await repository.record_delivery(999, 12345, "2026-10-22")

    assert await repository.has_delivery(999, 12345, "2026-10-22") is True
    assert await repository.has_delivery(999, 67890, "2026-10-22") is False

    repository.close()


@pytest.mark.asyncio
async def test_recording_duplicate_delivery_does_not_fail():
    """Test that recording the same delivery twice is safe."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    await repository.record_delivery(999, 12345, "2026-10-22")
    await repository.record_delivery(999, 12345, "2026-10-22")

    assert await repository.has_delivery(999, 12345, "2026-10-22") is True

    repository.close()


@pytest.mark.asyncio
async def test_delivery_persists_across_repository_instances(tmp_path):
    """Test that deliveries persist across repository instances."""

    database_path = tmp_path / "activity_tracker.db"

    first_repository = SQLiteReminderDeliveryRepository(str(database_path))

    await first_repository.record_delivery(999, 12345, "2026-10-22")
    first_repository.close()

    second_repository = SQLiteReminderDeliveryRepository(str(database_path))

    assert await second_repository.has_delivery(
        999,
        12345,
        "2026-10-22",
    ) is True

    second_repository.close()


def test_repository_can_be_closed():
    """Test that the repository can be closed cleanly."""

    repository = SQLiteReminderDeliveryRepository(":memory:")

    repository.close()
