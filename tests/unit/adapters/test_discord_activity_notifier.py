from unittest.mock import AsyncMock, Mock

from discord_habit_tracker.adapters.discord_activity_notifier import (
    DiscordActivityNotifier,
)


async def test_notifier_sends_notification_to_existing_channel():
    """Test that the notifier sends a notification to the existing activity channel."""

    channel = Mock()
    channel.name = "daily-streak"
    channel.send = AsyncMock()

    guild = Mock()
    guild.text_channels = [channel]
    guild.get_member.return_value = Mock(mention="<@12345>")
    guild.create_text_channel = AsyncMock()

    notifier = DiscordActivityNotifier()

    await notifier.notify(
        guild,
        user_id=12345,
        current_streak=4,
    )

    channel.send.assert_awaited_once_with(
        "🎉 <@12345> completed today's activity! Current streak: **4 days**."
    )
    guild.create_text_channel.assert_not_awaited()


async def test_notifier_creates_channel_if_missing():
    """Test that the notifier creates the activity channel if it doesn't exist."""

    channel = Mock()
    channel.name = "daily-streak"
    channel.send = AsyncMock()

    guild = Mock()
    guild.text_channels = []
    guild.get_member.return_value = Mock(mention="<@12345>")
    guild.create_text_channel = AsyncMock(return_value=channel)

    notifier = DiscordActivityNotifier()

    await notifier.notify(
        guild,
        user_id=12345,
        current_streak=4,
    )

    guild.create_text_channel.assert_awaited_once_with("daily-streak")

    channel.send.assert_awaited_once_with(
        "🎉 <@12345> completed today's activity! Current streak: **4 days**."
    )


async def test_notifier_uses_user_id_mention_when_member_is_not_cached():
    """Test that the notifier still mentions a member who isn't cached."""

    channel = Mock()
    channel.name = "daily-streak"
    channel.send = AsyncMock()

    guild = Mock()
    guild.text_channels = [channel]
    guild.get_member.return_value = None

    notifier = DiscordActivityNotifier()

    await notifier.notify(
        guild,
        user_id=12345,
        current_streak=4,
    )

    channel.send.assert_awaited_once_with(
        "🎉 <@12345> completed today's activity! Current streak: **4 days**."
    )


async def test_notifier_sends_reminder_to_existing_channel():
    """Test that a streak reminder is sent to the existing activity channel."""

    channel = Mock()
    channel.name = "daily-streak"
    channel.send = AsyncMock()

    guild = Mock()
    guild.text_channels = [channel]
    guild.get_member.return_value = Mock(mention="<@12345>")
    guild.create_text_channel = AsyncMock()

    notifier = DiscordActivityNotifier()

    await notifier.notify_reminder(
        guild,
        user_id=12345,
        current_streak=4,
    )

    channel.send.assert_awaited_once_with(
        "🔥 <@12345>, your current streak is **4 days**! "
        "Record today's activity to keep it going."
    )
    guild.create_text_channel.assert_not_awaited()


async def test_notifier_creates_channel_for_reminder_if_missing():
    """Test that a reminder creates the activity channel if necessary."""

    channel = Mock()
    channel.name = "daily-streak"
    channel.send = AsyncMock()

    guild = Mock()
    guild.text_channels = []
    guild.get_member.return_value = Mock(mention="<@12345>")
    guild.create_text_channel = AsyncMock(return_value=channel)

    notifier = DiscordActivityNotifier()

    await notifier.notify_reminder(
        guild,
        user_id=12345,
        current_streak=4,
    )

    guild.create_text_channel.assert_awaited_once_with("daily-streak")
    channel.send.assert_awaited_once_with(
        "🔥 <@12345>, your current streak is **4 days**! "
        "Record today's activity to keep it going."
    )


async def test_notifier_uses_user_id_mention_for_reminder_when_member_is_not_cached():
    """Test that a reminder mentions a member who isn't cached."""

    channel = Mock()
    channel.name = "daily-streak"
    channel.send = AsyncMock()

    guild = Mock()
    guild.text_channels = [channel]
    guild.get_member.return_value = None

    notifier = DiscordActivityNotifier()

    await notifier.notify_reminder(
        guild,
        user_id=12345,
        current_streak=4,
    )

    channel.send.assert_awaited_once_with(
        "🔥 <@12345>, your current streak is **4 days**! "
        "Record today's activity to keep it going."
    )
