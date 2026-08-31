import discord
from unittest.mock import AsyncMock, Mock
from datetime import datetime, timezone

from discord_habit_tracker.discord_gateway import DiscordGateway, MessageEvent


def test_gateway_initializes():
    """Test that the Discord Gateway initializes successfully."""

    gateway = DiscordGateway("test-token", Mock())

    assert gateway is not None


def test_gateway_creates_discord_client():
    """Test that the Discord Gateway creates a Discord client."""

    gateway = DiscordGateway("test-token", Mock())

    assert isinstance(gateway._client, discord.Client)


def test_gateway_enables_message_content_intent():
    """Test that the Discord Gateway enables the message content intent."""

    gateway = DiscordGateway("test-token", Mock())

    assert gateway._client.intents.message_content is True


async def test_gateway_starts_client():
    """Test that the Discord Gateway starts the Discord client."""

    gateway = DiscordGateway("test-token", Mock())

    gateway._client.start = AsyncMock()

    await gateway.start()

    gateway._client.start.assert_awaited_once_with("test-token")


def test_on_message_registers_client_event(monkeypatch):

    """Test that the Gateway registers its message handler with the client."""

    mock_client = Mock()

    monkeypatch.setattr(discord, "Client", Mock(return_value=mock_client))

    gateway = DiscordGateway("test-token", Mock())

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
    gateway = DiscordGateway("test-token", mock_handler)

    await gateway._on_message(mock_message)


    mock_handler.assert_awaited_once_with(expected_event)
