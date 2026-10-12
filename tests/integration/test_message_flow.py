from datetime import date, datetime, timezone

from discord_habit_tracker.event_listener import EventListener
from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.repositories.activity_repository import ActivityRepository
from discord_habit_tracker.services.activity_qualification_service import ActivityQualificationService
from discord_habit_tracker.services.activity_date_resolver import ActivityDateResolver
from discord_habit_tracker.repositories.membership_repository import MembershipRepository
from discord_habit_tracker.services.activity_stats_service import ActivityStatsService
from discord_habit_tracker.services.streak_service import StreakService


async def test_first_message_is_recorded():
    """Test that the first message from the tracked member is recorded."""

    # Arrange
    repository = ActivityRepository()
    qualification_service = ActivityQualificationService()
    date_resolver = ActivityDateResolver()
    membership_repository = MembershipRepository()

    await membership_repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    listener = EventListener(
        repository,
        membership_repository=membership_repository,  # No membership check needed for this test
        activity_qualification_service=qualification_service,
        activity_date_resolver=date_resolver,
    )

    event = MessageEvent(
        guild_id=999,
        user_id=12345,
        timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
    )

    # Act
    await listener.handle_message(event)

    # Assert
    result = await repository.has_activity_for_date(
        event.guild_id,
        event.user_id,
        event.timestamp.date(),
    )

    assert result is True


async def test_message_is_recorded_using_members_local_date():
    """Test that activity uses the member's local calendar date."""

    # Arrange
    repository = ActivityRepository()
    qualification_service = ActivityQualificationService()
    date_resolver = ActivityDateResolver()
    membership_repository = MembershipRepository()

    await membership_repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    listener = EventListener(
        repository,
        membership_repository=membership_repository,
        activity_qualification_service=qualification_service,
        activity_date_resolver=date_resolver,
    )

    event = MessageEvent(
        guild_id=999,
        user_id=12345,
        timestamp=datetime(
            2026, 8, 31, 18, 0,
            tzinfo=timezone.utc,
        ),
    )

    # Act
    await listener.handle_message(event)

    # Assert
    local_date = date(2026, 9, 1)

    result = await repository.has_activity_for_date(
        event.guild_id,
        event.user_id,
        local_date,
    )

    assert result is True


async def test_consecutive_local_activity_dates_produce_current_streak():
    """Test that messages on three consecutive local dates produce a three-day streak."""

    # Arrange
    repository = ActivityRepository()
    qualification_service = ActivityQualificationService()
    date_resolver = ActivityDateResolver()
    membership_repository = MembershipRepository()

    await membership_repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    listener = EventListener(
        repository,
        membership_repository=membership_repository,
        activity_qualification_service=qualification_service,
        activity_date_resolver=date_resolver,
    )

    events = [
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 8, 31, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 9, 1, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 9, 2, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
    ]

    stats_service = ActivityStatsService(
        repository,
        StreakService(),
    )

    # Act
    for event in events:
        await listener.handle_message(event)

    result = await stats_service.get_current_streak(
        guild_id=999,
        user_id=12345,
        current_date=date(2026, 9, 3),
    )

    # Assert
    assert result == 3


async def test_missing_activity_day_breaks_current_streak_but_preserves_longest():
    """Test that a missing day breaks the current streak without reducing the longest streak."""

    # Arrange
    repository = ActivityRepository()
    qualification_service = ActivityQualificationService()
    date_resolver = ActivityDateResolver()
    membership_repository = MembershipRepository()

    await membership_repository.add_member(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    listener = EventListener(
        repository,
        membership_repository=membership_repository,
        activity_qualification_service=qualification_service,
        activity_date_resolver=date_resolver,
    )

    events = [
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 8, 31, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 9, 1, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 9, 2, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
        # No activity on 4 September.
        MessageEvent(
            guild_id=999,
            user_id=12345,
            timestamp=datetime(
                2026, 9, 4, 18, 0,
                tzinfo=timezone.utc,
            ),
        ),
    ]

    stats_service = ActivityStatsService(
        repository,
        StreakService(),
    )

    # Act
    for event in events:
        await listener.handle_message(event)

    current_streak = await stats_service.get_current_streak(
        guild_id=999,
        user_id=12345,
        current_date=date(2026, 9, 5),
    )

    longest_streak = await stats_service.get_longest_streak(
        guild_id=999,
        user_id=12345,
    )

    # Assert
    assert current_streak == 1
    assert longest_streak == 3
