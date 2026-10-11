from discord_habit_tracker.repositories.sqlite_membership_repository import SQLiteMembershipRepository
from discord_habit_tracker.models.tracker_member import TrackerMember


async def test_added_member_can_be_found():
    """Test that an added member can be found."""

    repository = SQLiteMembershipRepository(":memory:")

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )

    result = await repository.get_member(999, 12345)

    assert result == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )


async def test_missing_member_cannot_be_found():
    """Test that an unregistered member is not found."""

    repository = SQLiteMembershipRepository(":memory:")

    result = await repository.get_member(999, 12345)

    assert result is None


async def test_different_guilds_are_tracked_separately():
    """Test that membership in different guilds is tracked independently."""

    repository = SQLiteMembershipRepository(":memory:")

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )

    assert await repository.get_member(999, 12345) is not None
    assert await repository.get_member(1000, 12345) is None


async def test_removed_member_cannot_be_found():
    """Test that removing a member removes their membership."""

    repository = SQLiteMembershipRepository(":memory:")

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )
    await repository.remove_member(999, 12345)

    result = await repository.get_member(999, 12345)

    assert result is None


async def test_membership_persists_across_repository_instances(tmp_path):
    """Test that membership persists across repository instances."""

    database_path = tmp_path / "activity_tracker.db"

    first_repository = SQLiteMembershipRepository(str(database_path))

    await first_repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )

    second_repository = SQLiteMembershipRepository(str(database_path))

    result = await second_repository.get_member(999, 12345)

    assert result == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",

    )


async def test_adding_duplicate_member_does_not_fail():
    """Test that adding the same member twice is safe."""

    repository = SQLiteMembershipRepository(":memory:")

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )

    result = await repository.get_member(999, 12345)

    assert result == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )


async def test_member_timezone_can_be_updated():
    """Test that updating a member changes their stored timezone."""

    repository = SQLiteMembershipRepository(":memory:")

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )

    await repository.update_timezone(
        999,
        12345,
        "Asia/Tokyo",
    )

    result = await repository.get_member(999, 12345)

    assert result == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Tokyo",
    )


async def test_updating_timezone_does_not_affect_other_members():
    """Test that updating one member's timezone leaves other members unchanged."""

    repository = SQLiteMembershipRepository(":memory:")

    await repository.add_member(
        999,
        12345,
        "Asia/Singapore",
    )
    await repository.add_member(
        999,
        67890,
        "Asia/Hong_Kong",
    )

    await repository.update_timezone(
        999,
        12345,
        "Asia/Tokyo",
    )

    updated_member = await repository.get_member(999, 12345)
    unchanged_member = await repository.get_member(999, 67890)

    assert updated_member == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Tokyo",
    )
    assert unchanged_member == TrackerMember(
        guild_id=999,
        user_id=67890,
        timezone="Asia/Hong_Kong",
    )


def test_repository_can_be_closed(tmp_path):
    """Test that the repository closes its database connection."""

    database_path = tmp_path / "activity_tracker.db"

    repository = SQLiteMembershipRepository(str(database_path))

    repository.close()

    assert repository._connection is None
