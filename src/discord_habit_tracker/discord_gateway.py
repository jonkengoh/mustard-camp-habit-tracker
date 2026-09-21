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
        timezone_name: str,
    ):
        """Initialize the Discord gateway."""

        self._bot_token = bot_token
        self._message_handler = message_handler

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        print("Messages intent:", intents.messages)
        print("Message content intent:", intents.message_content)

        self._client = discord.Client(intents=intents)
        self._tree = discord.app_commands.CommandTree(self._client)

        self._client.event(self.on_message)
        print("Registered on_message handler")
        self._client.event(self.on_ready)
        self._client.setup_hook = self._setup_hook

        self._streak_slash_command = DiscordStreakSlashCommand(
            streak_command,
            CurrentDateResolver(),
            timezone_name,
        )

        async def streak(interaction: discord.Interaction):
            await self._streak_slash_command.handle(interaction)

        self._tree.add_command(
            discord.app_commands.Command(
                name="streak",
                description="Show your current and longest activity streaks.",
                callback=streak,
            )
        )

    async def start(self):
        """Start the Discord client."""

        print("Starting Discord client...")
        await self._client.start(self._bot_token)
        print("Discord client stopped.")

    async def on_message(self, message):
        """Translate a Discord message into an application event."""


        print(
            f"Received message from {message.author.id}: {message.content}"
        )

        event = MessageEvent(
            user_id=message.author.id,
            timestamp=message.created_at,
        )

        await self._message_handler(event)

    async def on_ready(self):
        """Handle the Discord client becoming ready."""

        print(f"Logged in as {self._client.user}")

    async def _setup_hook(self):
        """Sync application commands with Discord."""

        print("Starting command sync...")
        await self._tree.sync()
        print("Command sync complete.")
