from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from discord_habit_tracker.timezones import (
    TIMEZONE_OPTIONS,
    format_timezone_label,
)


def test_all_timezone_options_use_valid_iana_timezones():
    for option in TIMEZONE_OPTIONS:
        ZoneInfo(option.timezone)


def test_timezone_options_are_not_empty():
    assert TIMEZONE_OPTIONS


def test_all_timezone_options_have_a_flag():
    for option in TIMEZONE_OPTIONS:
        assert option.flag


def test_all_timezone_options_use_unique_timezones():
    timezones = [option.timezone for option in TIMEZONE_OPTIONS]

    assert len(timezones) == len(set(timezones))


def test_timezone_label_includes_current_utc_offset():
    singapore = TIMEZONE_OPTIONS[0]

    now = datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc)

    result = format_timezone_label(singapore, now)

    assert result == "🇸🇬 Singapore (UTC+08:00)"


def test_timezone_label_accounts_for_daylight_saving_time_summer():
    london = next(
        option
        for option in TIMEZONE_OPTIONS
        if option.timezone == "Europe/London"
    )

    summer = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)

    result = format_timezone_label(london, summer)

    assert result == "🇬🇧 London (UTC+01:00)"


def test_timezone_label_accounts_for_daylight_saving_time_winter():
    london = next(
        option
        for option in TIMEZONE_OPTIONS
        if option.timezone == "Europe/London"
    )

    winter = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    result = format_timezone_label(london, winter)

    assert result == "🇬🇧 London (UTC+00:00)"
