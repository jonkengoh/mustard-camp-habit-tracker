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


async def test_membership_repository_returns_members_with_reminders_enabled():
    """Test that only members who opted in are returned."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )
    await repository.add_member(
        guild_id=999,
        user_id=67890,
        timezone="America/Los_Angeles",
    )

    await repository.set_reminders_enabled(
        guild_id=999,
        user_id=12345,
        enabled=True,
    )

    result = await repository.get_members_with_reminders_enabled()

    assert result == [
        TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
            reminders_enabled=True,
        )
    ]


async def test_membership_repository_returns_opted_in_members_across_guilds():
    """Test that opted-in memberships in different guilds are preserved."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )
    await repository.add_member(
        guild_id=888,
        user_id=12345,
        timezone="America/Los_Angeles",
    )

    await repository.set_reminders_enabled(999, 12345, True)
    await repository.set_reminders_enabled(888, 12345, True)

    result = await repository.get_members_with_reminders_enabled()

    assert set(result) == {
        TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
            reminders_enabled=True,
        ),
        TrackerMember(
            guild_id=888,
            user_id=12345,
            timezone="America/Los_Angeles",
            reminders_enabled=True,
        ),
    }


async def test_membership_repository_returns_empty_list_when_no_members_opted_in():
    """Test that no members are returned when nobody opted in."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    result = await repository.get_members_with_reminders_enabled()

    assert result == []
