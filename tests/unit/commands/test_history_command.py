from datetime import date
from unittest.mock import AsyncMock, Mock

import pytest

from discord_habit_tracker.commands.history_command import HistoryCommand


@pytest.mark.asyncio
async def test_history_command_returns_activity_for_requested_date_range():
    """Display activity for each day in the requested date range."""

    activity_repository = Mock()
    activity_repository.get_activity_dates_in_range = AsyncMock(
        return_value={
            date(2026, 10, 15),
            date(2026, 10, 17),
        }
    )

    command = HistoryCommand(activity_repository)

    result = await command.handle(
        guild_id=999,
        user_id=12345,
        start_date=date(2026, 10, 15),
        end_date=date(2026, 10, 17),
    )

    assert result == (
        "Activity History (15 Oct – 17 Oct 2026)\n"
        "✓ Sat, 17 Oct\n"
        "✗ Fri, 16 Oct\n"
        "✓ Thu, 15 Oct\n"
        "\n"
        "Active days: 2/3 (66.7%)"
    )

    activity_repository.get_activity_dates_in_range.assert_awaited_once_with(
        999,
        12345,
        date(2026, 10, 15),
        date(2026, 10, 17),
    )


@pytest.mark.asyncio
async def test_history_command_returns_no_activity_message_when_history_is_empty():
    """Report that no activity was recorded in the requested range."""

    activity_repository = Mock()
    activity_repository.get_activity_dates_in_range = AsyncMock(
        return_value=set()
    )

    command = HistoryCommand(activity_repository)

    result = await command.handle(
        guild_id=999,
        user_id=12345,
        start_date=date(2026, 10, 15),
        end_date=date(2026, 10, 17),
    )

    assert result == (
        "Activity History (15 Oct – 17 Oct 2026)\n"
        "No activity recorded during this period.\n"
        "\n"
        "Active days: 0/3 (0.0%)"
    )


@pytest.mark.asyncio
async def test_history_command_displays_all_days_including_inactive_days():
    """Include inactive days so the history shows gaps in activity."""

    activity_repository = Mock()
    activity_repository.get_activity_dates_in_range = AsyncMock(
        return_value={date(2026, 10, 17)}
    )

    command = HistoryCommand(activity_repository)

    result = await command.handle(
        guild_id=999,
        user_id=12345,
        start_date=date(2026, 10, 15),
        end_date=date(2026, 10, 17),
    )

    assert "✓ Sat, 17 Oct" in result
    assert "✗ Fri, 16 Oct" in result
    assert "✗ Thu, 15 Oct" in result


@pytest.mark.asyncio
async def test_history_command_handles_single_day_range():
    """Calculate activity rate correctly for a one-day range."""

    activity_repository = Mock()
    activity_repository.get_activity_dates_in_range = AsyncMock(
        return_value={date(2026, 10, 17)}
    )

    command = HistoryCommand(activity_repository)

    result = await command.handle(
        guild_id=999,
        user_id=12345,
        start_date=date(2026, 10, 17),
        end_date=date(2026, 10, 17),
    )

    assert result == (
        "Activity History (17 Oct 2026)\n"
        "✓ Sat, 17 Oct\n"
        "\n"
        "Active days: 1/1 (100.0%)"
    )


@pytest.mark.asyncio
async def test_history_command_rejects_reversed_date_range():
    """Reject a range whose start date is after its end date."""

    activity_repository = Mock()
    activity_repository.get_activity_dates_in_range = AsyncMock()

    command = HistoryCommand(activity_repository)

    with pytest.raises(ValueError, match="start_date must be on or before end_date"):
        await command.handle(
            guild_id=999,
            user_id=12345,
            start_date=date(2026, 10, 18),
            end_date=date(2026, 10, 17),
        )

    activity_repository.get_activity_dates_in_range.assert_not_awaited()
