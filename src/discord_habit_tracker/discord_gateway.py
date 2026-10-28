"""
Discord gateway adapter.

Responsible for communicating between Discord and the application layer.

Responsibilities:
    - Configure and start the Discord client
    - Register Discord event listeners
    - Translate Discord events into application events
    - Register Discord application commands
    - Forward command interactions to the application layer

This module contains no business logic.
"""

# =============================================================================
# Imports
# =============================================================================

import asyncio
import discord

from discord_habit_tracker.commands.discord_streak_slash_command import (
    DiscordStreakSlashCommand,
)
from discord_habit_tracker.commands.discord_streak_join_slash_command import (
    DiscordStreakJoinSlashCommand,
)
from discord_habit_tracker.commands.discord_streak_leave_slash_command import (
    DiscordStreakLeaveSlashCommand,
)

from discord_habit_tracker.commands.discord_streak_timezone_slash_command import (
    DiscordStreakTimezoneSlashCommand,
)

from discord_habit_tracker.commands.discord_history_slash_command import (
    DiscordHistorySlashCommand,
)

from discord_habit_tracker.models.message_event import MessageEvent
from discord_habit_tracker.services.current_date_resolver import CurrentDateResolver



# =============================================================================
# Discord Gateway
# =============================================================================

class DiscordGateway:
    """Adapter between Discord and the application layer."""

    def __init__(
        self,
        bot_token: str,
        message_handler,
        streak_command,
        history_command,
        membership_repository,
        membership_service,
        activity_stats_service,
        activity_notifier,
        reminder_scheduler=None,
    ):
        """Initialize the Discord gateway."""

        self._bot_token = bot_token
        self._message_handler = message_handler
        self._history_command = history_command
        self._membership_repository = membership_repository
        self._membership_service = membership_service
        self._activity_stats_service = activity_stats_service
        self._activity_notifier = activity_notifier
        self._reminder_scheduler = reminder_scheduler
        self._reminder_task = None

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        self._client = discord.Client(intents=intents)
        self._tree = discord.app_commands.CommandTree(self._client)

        self._client.event(self.on_message)
        self._client.event(self.on_ready)
        self._client.setup_hook = self._setup_hook

        self._streak_slash_command = DiscordStreakSlashCommand(
            streak_command,
            CurrentDateResolver(),
            self._membership_repository,
        )

        self._streak_join_slash_command = DiscordStreakJoinSlashCommand(
            self._membership_service,
        )

        self._streak_leave_slash_command = DiscordStreakLeaveSlashCommand(
            self._membership_service,
        )

        self._streak_timezone_slash_command = DiscordStreakTimezoneSlashCommand(
            self._membership_service,
        )

        self._history_slash_command = DiscordHistorySlashCommand(
            self._history_command,
            CurrentDateResolver(),
            self._membership_repository,
        )

        streak_group = discord.app_commands.Group(
            name="streak",
            description="Manage your activity streak.",
        )

        async def stats(interaction: discord.Interaction):
            await self._streak_slash_command.handle(interaction)

        async def join(interaction: discord.Interaction):
            await self._streak_join_slash_command.handle(interaction)

        async def timezone(interaction: discord.Interaction):
            await self._streak_timezone_slash_command.handle(interaction)

        async def leave(interaction: discord.Interaction):
            await self._streak_leave_slash_command.handle(interaction)

        async def history(
            interaction: discord.Interaction,
            days: discord.app_commands.Range[int, 1, 30] = 7,
        ):
            await self._history_slash_command.handle(interaction, days)


        history_command = discord.app_commands.Command(
            name="history",
            description="Show your recent daily activity history.",
            callback=history,
        )

        self._tree.add_command(history_command)

        streak_group.add_command(
            discord.app_commands.Command(
                name="stats",
                description="Show your current and longest activity streaks.",
                callback=stats,
            )
        )

        streak_group.add_command(
            discord.app_commands.Command(
                name="join",
                description="Join the activity tracker.",
                callback=join,
            )
        )

        streak_group.add_command(
            discord.app_commands.Command(
                name="timezone",
                description="Change your tracker timezone.",
                callback=timezone,
            )
        )

        streak_group.add_command(
            discord.app_commands.Command(
                name="leave",
                description="Leave the activity tracker.",
                callback=leave,
            )
        )

        self._tree.add_command(streak_group)


    @property
    def client(self):
        """Expose the Discord client for application services."""
        return self._client

    def set_reminder_scheduler(self, reminder_scheduler):
        """Set the scheduler responsible for daily streak reminders."""
        self._reminder_scheduler = reminder_scheduler


    async def start(self):
        """Start the Discord client."""

        try:
            await self._client.start(self._bot_token)
        finally:
            if self._reminder_task is not None:
                self._reminder_task.cancel()

                try:
                    await self._reminder_task
                except asyncio.CancelledError:
                    pass


    async def on_message(self, message):
        """Translate a Discord message into an application event."""

        print(
            f"Received message from {message.author.id}: {message.content}"
        )

        event = MessageEvent(
            guild_id=message.guild.id,
            user_id=message.author.id,
            timestamp=message.created_at,
        )

        activity = await self._message_handler(event)

        if activity is None:
            return

        current_streak = await self._activity_stats_service.get_current_streak(
            activity.guild_id,
            activity.user_id,
            activity.activity_date,
        )

        await self._activity_notifier.notify(
            message.guild,
            user_id=activity.user_id,
            current_streak=current_streak,
        )

    async def on_ready(self):
        """Handle the Discord client becoming ready."""

        print(f"Logged in as {self._client.user}")

        if (
            self._reminder_scheduler is not None
            and (self._reminder_task is None or self._reminder_task.done())
        ):
            self._reminder_task = asyncio.create_task(
                self._reminder_scheduler.run()
            )

    async def _setup_hook(self):
        """Sync application commands with Discord."""

        await self._tree.sync()
