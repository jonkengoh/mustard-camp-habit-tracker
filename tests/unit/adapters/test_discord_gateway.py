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
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    assert gateway is not None


def test_gateway_creates_discord_client():
    """Test that the Discord Gateway creates a Discord client."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    assert isinstance(gateway._client, discord.Client)


def test_gateway_enables_message_content_intent():
    """Test that the Discord Gateway enables the message content intent."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    assert gateway._client.intents.message_content is True


async def test_gateway_starts_client():
    """Test that the Discord Gateway starts the Discord client."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
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
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    mock_client.event.assert_any_call(gateway.on_message)


async def test_translate_forward_discord_message():

    """Test that the gateway creates the MessageEvent and passes it to the async handler"""

    known_timestamp = datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc)

    mock_message = Mock()
    mock_message.guild.id = 999
    mock_message.author.id = 12345
    mock_message.created_at = known_timestamp



    # Construct event
    expected_event = MessageEvent(
        guild_id=999,
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
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    await gateway.on_message(mock_message)


    mock_handler.assert_awaited_once_with(expected_event)


def test_discord_gateway_registers_streak_command():
    streak_command = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=streak_command,
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
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
        membership_service=Mock(),
        membership_repository=Mock()
    )

    gateway._streak_slash_command = Mock()
    gateway._streak_slash_command.handle = AsyncMock()

    interaction = Mock()

    streak_group = next(
        command
        for command in gateway._tree.get_commands()
        if command.name == "streak"
    )

    stats_command = next(
        command
        for command in streak_group.commands
        if command.name == "stats"
    )

    await stats_command.callback(interaction)

    gateway._streak_slash_command.handle.assert_awaited_once_with(
        interaction,
    )


async def test_gateway_syncs_application_commands():

    """Test that the gateway syncs application commands with Discord."""

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    gateway._tree.sync = AsyncMock()

    await gateway._client.setup_hook()

    gateway._tree.sync.assert_awaited_once()


def test_streak_command_contains_join_subcommand():
    membership_service = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=membership_service,
        membership_repository=Mock(),
    )

    streak_command = next(
        command
        for command in gateway._tree.get_commands()
        if command.name == "streak"
    )

    assert isinstance(streak_command, discord.app_commands.Group)

    join_command = next(
        command
        for command in streak_command.commands
        if command.name == "join"
    )

    assert join_command is not None


def test_streak_command_contains_leave_subcommand():
    membership_service = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=membership_service,
        membership_repository=Mock(),
    )

    streak_command = next(
        command
        for command in gateway._tree.get_commands()
        if command.name == "streak"
    )

    assert isinstance(streak_command, discord.app_commands.Group)

    leave_command = next(
        command
        for command in streak_command.commands
        if command.name == "leave"
    )

    assert leave_command is not None


async def test_discord_gateway_leave_command_delegates_to_handler():
    """Test that the leave command delegates to the Discord adapter."""

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_service=Mock(),
        membership_repository=Mock(),
    )

    gateway._streak_leave_slash_command = Mock()
    gateway._streak_leave_slash_command.handle = AsyncMock()

    interaction = Mock()

    streak_group = next(
        command
        for command in gateway._tree.get_commands()
        if command.name == "streak"
    )

    leave_command = next(
        command
        for command in streak_group.commands
        if command.name == "leave"
    )

    await leave_command.callback(interaction)

    gateway._streak_leave_slash_command.handle.assert_awaited_once_with(
        interaction,
    )

def test_gateway_injects_membership_repository_into_streak_command():
    membership_repository = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        timezone_name="Asia/Singapore",
        membership_repository=membership_repository,
        membership_service=Mock(),
    )

    assert gateway._streak_slash_command._membership_repository is membership_repository
