import pytest

from discord_habit_tracker.models.tracker_member import TrackerMember
from discord_habit_tracker.repositories.membership_repository import MembershipRepository
from discord_habit_tracker.services.membership_service import MembershipService
from discord_habit_tracker.services.exceptions import (
    InvalidTimezoneError,
    MemberAlreadyExistsError,
    MemberNotFoundError,
)


async def test_join_adds_member():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    await service.join(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )

    member = await membership_repository.get_member(123, 456)

    assert member == TrackerMember(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )


async def test_join_rejects_existing_member():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    await membership_repository.add_member(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )

    with pytest.raises(MemberAlreadyExistsError):
        await service.join(
            guild_id=123,
            user_id=456,
            timezone="Asia/Tokyo",
        )

    member = await membership_repository.get_member(123, 456)

    assert member == TrackerMember(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )


async def test_join_rejects_invalid_timezone():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    with pytest.raises(InvalidTimezoneError):
        await service.join(
            guild_id=123,
            user_id=456,
            timezone="Not/A/Timezone",
        )

    member = await membership_repository.get_member(123, 456)

    assert member is None

async def test_leave_removes_member():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    await membership_repository.add_member(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )

    await service.leave(
        guild_id=123,
        user_id=456,
    )

    member = await membership_repository.get_member(123, 456)

    assert member is None

async def test_leave_rejects_non_member():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    with pytest.raises(MemberNotFoundError):
        await service.leave(
            guild_id=123,
            user_id=456,
        )

    member = await membership_repository.get_member(123, 456)

    assert member is None


async def test_update_timezone_changes_member_timezone():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    await membership_repository.add_member(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )

    await service.update_timezone(
        guild_id=123,
        user_id=456,
        timezone="Asia/Tokyo",
    )

    member = await membership_repository.get_member(123, 456)

    assert member == TrackerMember(
        guild_id=123,
        user_id=456,
        timezone="Asia/Tokyo",
    )


async def test_update_timezone_changes_member_timezone():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    await membership_repository.add_member(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )

    await service.update_timezone(
        guild_id=123,
        user_id=456,
        timezone="Asia/Tokyo",
    )

    member = await membership_repository.get_member(123, 456)

    assert member == TrackerMember(
        guild_id=123,
        user_id=456,
        timezone="Asia/Tokyo",
    )


async def test_update_timezone_rejects_non_member():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    with pytest.raises(MemberNotFoundError):
        await service.update_timezone(
            guild_id=123,
            user_id=456,
            timezone="Asia/Tokyo",
        )

    member = await membership_repository.get_member(123, 456)

    assert member is None


async def test_update_timezone_rejects_invalid_timezone():
    membership_repository = MembershipRepository()
    service = MembershipService(membership_repository)

    await membership_repository.add_member(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )

    with pytest.raises(InvalidTimezoneError):
        await service.update_timezone(
            guild_id=123,
            user_id=456,
            timezone="Not/A/Timezone",
        )

    member = await membership_repository.get_member(123, 456)

    assert member == TrackerMember(
        guild_id=123,
        user_id=456,
        timezone="Asia/Singapore",
    )
