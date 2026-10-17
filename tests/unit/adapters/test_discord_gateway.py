from datetime import date, datetime, timezone

from unittest.mock import AsyncMock, Mock

import discord

from discord_habit_tracker.discord_gateway import DiscordGateway
from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.models.activity_event import ActivityEvent
from discord_habit_tracker.models.tracker_member import TrackerMember


def test_gateway_initializes():
    """Test that the Discord Gateway initializes successfully."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    assert gateway is not None


def test_gateway_creates_discord_client():
    """Test that the Discord Gateway creates a Discord client."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    assert isinstance(gateway._client, discord.Client)


def test_gateway_enables_message_content_intent():
    """Test that the Discord Gateway enables the message content intent."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    assert gateway._client.intents.message_content is True


async def test_gateway_starts_client():
    """Test that the Discord Gateway starts the Discord client."""

    gateway = DiscordGateway(
        "test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
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
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
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

    mock_handler = AsyncMock(return_value=None)

    # Gateway initialize
    gateway = DiscordGateway(
        "test-token",
        mock_handler,
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    await gateway.on_message(mock_message)


    mock_handler.assert_awaited_once_with(expected_event)


def test_discord_gateway_registers_streak_command():
    """Test that the Discord Gateway registers the /streak command."""
    streak_command = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=streak_command,
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    registered_commands = gateway._tree.get_commands()

    assert len(registered_commands) == 2

    assert {command.name for command in registered_commands} == {
        "streak",
        "history",
    }


async def test_discord_gateway_streak_command_delegates_to_handler():
    """Test that the streak command delegates to the Discord adapter."""
    streak_command = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=streak_command,
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
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
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    gateway._tree.sync = AsyncMock()

    await gateway._client.setup_hook()

    gateway._tree.sync.assert_awaited_once()


def test_streak_command_contains_join_subcommand():
    """Test that the streak command contains the join subcommand."""
    membership_service = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=membership_service,
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
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
    """Test that the streak command contains the leave subcommand."""
    membership_service = Mock()

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=membership_service,
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
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
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

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
        history_command=Mock(),
        membership_repository=membership_repository,
        membership_service=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    assert gateway._streak_slash_command._membership_repository is membership_repository


def test_streak_command_contains_timezone_subcommand():
    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    streak_command = next(
        command
        for command in gateway._tree.get_commands()
        if command.name == "streak"
    )

    assert isinstance(streak_command, discord.app_commands.Group)

    timezone_command = next(
        command
        for command in streak_command.commands
        if command.name == "timezone"
    )

    assert timezone_command is not None


async def test_discord_gateway_timezone_command_delegates_to_handler():
    """Test that the timezone command delegates to its Discord adapter."""

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    gateway._streak_timezone_slash_command = Mock()
    gateway._streak_timezone_slash_command.handle = AsyncMock()

    interaction = Mock()

    streak_group = next(
        command
        for command in gateway._tree.get_commands()
        if command.name == "streak"
    )

    timezone_command = next(
        command
        for command in streak_group.commands
        if command.name == "timezone"
    )

    await timezone_command.callback(interaction)

    gateway._streak_timezone_slash_command.handle.assert_awaited_once_with(
        interaction,
    )


async def test_gateway_notifies_when_new_activity_is_recorded():
    """Test that a newly recorded activity triggers a streak notification."""

    activity = ActivityEvent(
        guild_id=999,
        user_id=12345,
        activity_date=date(2026, 10, 14),
    )

    message_handler = AsyncMock(return_value=activity)

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock(return_value=4)

    activity_notifier = Mock()
    activity_notifier.notify = AsyncMock()

    guild = Mock()

    message = Mock()
    message.guild = guild
    message.author.id = 12345
    message.created_at = datetime(
        2026, 10, 14, 2, 0, tzinfo=timezone.utc
    )
    message.content = "Hello!"

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=message_handler,
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=activity_stats_service,
        activity_notifier=activity_notifier,
    )

    await gateway.on_message(message)

    activity_stats_service.get_current_streak.assert_awaited_once_with(
        999,
        12345,
        date(2026, 10, 14),
    )

    activity_notifier.notify.assert_awaited_once_with(
        guild,
        user_id=12345,
        current_streak=4,
    )


async def test_gateway_does_not_notify_when_no_new_activity_is_recorded():
    """Test that the gateway skips notifications when no new activity is recorded."""

    message_handler = AsyncMock(return_value=None)

    activity_stats_service = Mock()
    activity_stats_service.get_current_streak = AsyncMock()

    activity_notifier = Mock()
    activity_notifier.notify = AsyncMock()

    message = Mock()
    message.guild.id = 999
    message.author.id = 12345
    message.created_at = datetime(
        2026, 10, 14, 2, 0, tzinfo=timezone.utc
    )
    message.content = "Hello!"

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=message_handler,
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=activity_stats_service,
        activity_notifier=activity_notifier,
    )

    await gateway.on_message(message)

    activity_stats_service.get_current_streak.assert_not_awaited()
    activity_notifier.notify.assert_not_awaited()


def test_discord_gateway_registers_history_command():
    """Test that /history is registered with the correct argument bounds."""
    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=Mock(),
        membership_service=Mock(),
        membership_repository=Mock(),
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    registered_commands = gateway._tree.get_commands()
    command = next(
        command
        for command in registered_commands
        if command.name == "history"
    )

    assert command.description == "Show your recent daily activity history."

    days_parameter = next(
        parameter
        for parameter in command.parameters
        if parameter.name == "days"
    )

    assert days_parameter.default == 7
    assert days_parameter.min_value == 1
    assert days_parameter.max_value == 30


async def test_discord_gateway_history_command_delegates_to_handler():
    """Test that /history delegates to the history slash-command handler."""
    history_command = AsyncMock()

    membership_repository = Mock()
    membership_repository.get_member = AsyncMock(
        return_value=TrackerMember(
            guild_id=999,
            user_id=12345,
            timezone="Asia/Singapore",
        )
    )

    gateway = DiscordGateway(
        bot_token="test-token",
        message_handler=Mock(),
        streak_command=Mock(),
        history_command=history_command,
        membership_service=Mock(),
        membership_repository=membership_repository,
        activity_stats_service=Mock(),
        activity_notifier=Mock(),
    )

    gateway._history_slash_command.handle = AsyncMock()

    registered_commands = gateway._tree.get_commands()
    command = next(
        command
        for command in registered_commands
        if command.name == "history"
    )

    interaction = Mock()
    interaction.guild.id = 999
    interaction.user.id = 12345
    interaction.response.send_message = AsyncMock()

    await command.callback(interaction, days=14)

    gateway._history_slash_command.handle.assert_awaited_once_with(
        interaction,
        14,
    )
