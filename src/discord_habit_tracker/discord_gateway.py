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
        membership_repository,
        membership_service,
    ):
        """Initialize the Discord gateway."""

        self._bot_token = bot_token
        self._message_handler = message_handler
        self._membership_repository = membership_repository
        self._membership_service = membership_service

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

        self._streak_timezone_slash_command = DiscordStreakTimezoneSlashCommand(
            self._membership_service,
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


    async def start(self):
        """Start the Discord client."""

        await self._client.start(self._bot_token)

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

        await self._message_handler(event)

    async def on_ready(self):
        """Handle the Discord client becoming ready."""

        print(f"Logged in as {self._client.user}")

    async def _setup_hook(self):
        """Sync application commands with Discord."""

        await self._tree.sync()
