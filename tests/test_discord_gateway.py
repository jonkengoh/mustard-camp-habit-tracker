from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import discord

from discord_habit_tracker.discord_gateway import DiscordGateway
from discord_habit_tracker.models.message_event import MessageEvent


def test_gateway_initializes():
    """Test that the Discord Gateway initializes successfully."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore"
    )

    assert gateway is not None


def test_gateway_creates_discord_client():
    """Test that the Discord Gateway creates a Discord client."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
    )

    assert isinstance(gateway._client, discord.Client)


def test_gateway_enables_message_content_intent():
    """Test that the Discord Gateway enables the message content intent."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
    )

    assert gateway._client.intents.message_content is True


async def test_gateway_starts_client():
    """Test that the Discord Gateway starts the Discord client."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
    )

    gateway._client.start = AsyncMock()

    await gateway.start()

    gateway._client.start.assert_awaited_once_with("test-token")


def test_on_message_registers_client_event(monkeypatch):
    """Test that the Gateway registers its message handler with the client."""

    mock_client = Mock()
    mock_tree = Mock()

    monkeypatch.setattr(
        discord,
        "Client",
        Mock(return_value=mock_client),
    )

    monkeypatch.setattr(
        discord.app_commands,
        "CommandTree",
        Mock(return_value=mock_tree),
    )

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
    )

    mock_client.event.assert_called_once_with(gateway._on_message)


async def test_translate_forward_discord_message():

    """Test that the gateway creates the MessageEvent and passes it to the async handler"""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    mock_message = Mock()
    mock_message.author.id = 12345
    mock_message.created_at = known_timestamp



    # Construct event
    expected_event = MessageEvent(
        user_id=12345,
        timestamp=known_timestamp,
    )

    mock_handler = AsyncMock()

    # Gateway initialize
    gateway = DiscordGateway(
        "test-token",
        mock_handler,
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
    )

    await gateway._on_message(mock_message)


    mock_handler.assert_awaited_once_with(expected_event)


def test_discord_gateway_registers_streak_command():
    streak_command = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=streak_command,
        timezone_name="Asia/Singapore",
    )

    registered_commands = gateway._tree.get_commands()

    assert len(registered_commands) == 1

    command = registered_commands[0]

    assert command.name == "streak"


async def test_discord_gateway_streak_command_delegates_to_handler():
    """Test that the streak command delegates to the Discord adapter."""
    streak_command = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=streak_command,
        timezone_name="Asia/Singapore",
    )

    gateway._streak_slash_command = Mock()
    gateway._streak_slash_command.handle = AsyncMock()

    interaction = Mock()

    registered_commands = gateway._tree.get_commands()
    command = registered_commands[0]

    await command.callback(interaction)

    gateway._streak_slash_command.handle.assert_awaited_once_with(
        interaction,
    )
