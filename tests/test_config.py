import pytest

from discord_habit_tracker.config import Config


def test_config_loads_bot_token(monkeypatch):
    """Test a valid token:

    Change environment only for this test using setenv"""
    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_ID", "12345")

    config = Config()

    assert config.bot_token == "test-token"


def test_config_requires_bot_token(monkeypatch):
    """Test missing-token case:

    Remove DISCORD_TOKEN from the test environment,
    then verify that creating Config raises ValueError."""
    monkeypatch.delenv("DISCORD_TOKEN", raising=False)

    with pytest.raises(ValueError):
        Config()


def test_config_loads_tracked_user_id(monkeypatch):
    """Test that the tracked user ID is loaded and converted to an integer."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_ID", "12345")

    config = Config()

    assert config.tracked_user_id == 12345


def test_config_requires_tracked_user_id(monkeypatch):
    """Test that a missing tracked user ID raises ValueError."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.delenv("DISCORD_TRACKED_USER_ID", raising=False)

    with pytest.raises(ValueError):
        Config()


def test_config_requires_valid_tracked_user_id(monkeypatch):
    """Test that an invalid tracked user ID raises ValueError."""

    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setenv("DISCORD_TRACKED_USER_ID", "not-a-number")

    with pytest.raises(
        ValueError,
        match="DISCORD_TRACKED_USER_ID must be a valid integer.",
    ):
        Config()
