import discord
from unittest.mock import AsyncMock

from discord_habit_tracker.discord_gateway import DiscordGateway


def test_gateway_initializes():
    """Test that the Discord Gateway initializes successfully."""

    gateway = DiscordGateway("test-token")

    assert gateway is not None


def test_gateway_creates_discord_client():
    """Test that the Discord Gateway creates a Discord client."""

    gateway = DiscordGateway("test-token")

    assert isinstance(gateway._client, discord.Client)


def test_gateway_enables_message_content_intent():
    """Test that the Discord Gateway enables the message content intent."""

    gateway = DiscordGateway("test-token")

    assert gateway._client.intents.message_content is True


async def test_gateway_starts_client():
    """Test that the Discord Gateway starts the Discord client."""

    gateway = DiscordGateway("test-token")

    gateway._client.start = AsyncMock()

    await gateway.start()

    gateway._client.start.assert_awaited_once_with("test-token")
