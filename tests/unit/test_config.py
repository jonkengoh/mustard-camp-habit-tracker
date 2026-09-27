import pytest

from discord_habit_tracker.config import Config


def test_config_loads_bot_token(monkeypatch):
    """Test a valid token:

    Change environment only for this test using setenv"""
    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_IDS", "12345")

    config = Config()

    assert config.bot_token == "test-token"


def test_config_requires_bot_token(monkeypatch):
    """Test missing-token case:

    Remove DISCORD_TOKEN from the test environment,
    then verify that creating Config raises ValueError."""
    monkeypatch.delenv("DISCORD_TOKEN", raising=False)

    with pytest.raises(ValueError):
        Config()


def test_config_loads_tracked_member_timezone(monkeypatch):
    """Test that Config loads the tracked member's timezone."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_IDS", "12345")
    monkeypatch.setenv(
        "DISCORD_TRACKED_USER_TIMEZONE",
        "America/Chicago",
    )

    config = Config()

    assert config.tracked_user_timezone == "America/Chicago"

