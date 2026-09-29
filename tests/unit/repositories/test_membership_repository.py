from discord_habit_tracker.repositories.membership_repository import MembershipRepository
from discord_habit_tracker.models.tracker_member import TrackerMember


async def test_membership_repository_adds_member():
    """Test that a user can join a guild's tracker."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    result = await repository.get_member(
        guild_id=999,
        user_id=12345,
    )

    assert result == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )


async def test_membership_repository_isolates_guilds():
    """Test that membership is scoped to a guild."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    assert await repository.get_member(
        guild_id=999,
        user_id=12345,
    ) == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    assert await repository.get_member(
        guild_id=888,
        user_id=12345,
    ) is None


async def test_membership_repository_isolates_users():
    """Test that membership is scoped to a user."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    assert await repository.get_member(
        guild_id=999,
        user_id=12345,
    ) == TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    assert await repository.get_member(
        guild_id=999,
        user_id=67890,
    ) is None


async def test_membership_repository_removes_member():
    """Test that a user can leave a guild's tracker."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    await repository.remove_member(
        guild_id=999,
        user_id=12345,
    )

    result = await repository.get_member(
        guild_id=999,
        user_id=12345,
    )

    assert result is None


async def test_membership_repository_returns_none_for_missing_member():
    """Test that an unregistered member cannot be retrieved."""

    repository = MembershipRepository()

    result = await repository.get_member(
        guild_id=999,
        user_id=12345,
    )

    assert result is None
