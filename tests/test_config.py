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


def test_config_loads_tracked_user_ids(monkeypatch):
    """Test that multiple tracked user IDs are loaded as integers."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_IDS", "12345,67890")

    config = Config()

    assert config.tracked_user_ids == {12345, 67890}


def test_config_requires_tracked_user_ids(monkeypatch):
    """Test that a missing tracked user ID raises ValueError."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.delenv("DISCORD_TRACKED_USER_IDS", raising=False)

    with pytest.raises(ValueError):
        Config()


def test_config_requires_valid_tracked_user_ids(monkeypatch):
    """Test that an invalid tracked user ID raises ValueError."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_IDS", "not-a-number")

    with pytest.raises(
        ValueError,
        match="DISCORD_TRACKED_USER_IDS must contain valid integers.",
    ):
        Config()


def test_config_loads_tracked_user_timezone(monkeypatch):
    """Test that Config loads the tracked user's timezone."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_IDS", "12345")
    monkeypatch.setenv(
        "DISCORD_TRACKED_USER_TIMEZONE",
        "America/Chicago",
    )

    config = Config()

    assert config.tracked_user_timezone == "America/Chicago"


def test_config_requires_all_tracked_user_ids_to_be_valid(monkeypatch):
    """Test that every tracked user ID must be a valid integer."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv(
        "DISCORD_TRACKED_USER_IDS",
        "12345,not-a-number,67890",
    )

    with pytest.raises(
        ValueError,
        match="DISCORD_TRACKED_USER_IDS must contain valid integers.",
    ):
        Config()
