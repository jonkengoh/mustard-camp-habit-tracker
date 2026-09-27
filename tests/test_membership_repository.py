import pytest

from discord_habit_tracker.repositories.membership_repository import (
    MembershipRepository,
)

@pytest.mark.asyncio
async def test_membership_repository_adds_member():
    """Test that a user can join a guild's tracker."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
    )

    result = await repository.is_member(
        guild_id=999,
        user_id=12345,
    )

    assert result is True


@pytest.mark.asyncio
async def test_membership_repository_isolates_guilds():
    """Test that membership is scoped to a guild."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
    )

    assert await repository.is_member(
        guild_id=999,
        user_id=12345,
    ) is True

    assert await repository.is_member(
        guild_id=888,
        user_id=12345,
    ) is False


@pytest.mark.asyncio
async def test_membership_repository_isolates_users():
    """Test that membership is scoped to a user."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
    )

    assert await repository.is_member(
        guild_id=999,
        user_id=12345,
    ) is True

    assert await repository.is_member(
        guild_id=999,
        user_id=67890,
    ) is False


@pytest.mark.asyncio
async def test_membership_repository_removes_member():
    """Test that a user can leave a guild's tracker."""

    repository = MembershipRepository()

    await repository.add_member(
        guild_id=999,
        user_id=12345,
    )

    await repository.remove_member(
        guild_id=999,
        user_id=12345,
    )

    result = await repository.is_member(
        guild_id=999,
        user_id=12345,
    )

    assert result is False
