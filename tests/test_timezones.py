from zoneinfo import ZoneInfo

from discord_habit_tracker.timezones import TIMEZONE_OPTIONS


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
