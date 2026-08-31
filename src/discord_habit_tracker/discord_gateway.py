'''
Discord Gateway

Provides communication between the application and Discord.

Responsibilities:

    - Connect to Discord

    - Receive Discord events

    - Forward events to the application layer

    - Send messages back to Discord

This module intentionally contains no business logic.

Goal: Track specific discord
 username and record the FIRST message
 event instance for the current date.'''

"""
discord_gateway.py

Purpose:
    Responsible for communicating with Discord.

Responsibilities:
    - Connect to Discord Gateway
    - Register event listeners
    - Receive Discord events
    - Forward events to the application layer
    - Send responses back to Discord when requested

Non-Responsibilities:
    - Business logic
    - Database operations
    - Streak calculations
    - Activity qualification
    - Statistics generation

Author:
    Jonathan Goh

Version:
    v0.1
"""

# =============================================================================
# Imports
# =============================================================================

# Standard library imports


# Third-party imports
# (discord.py, dotenv, etc.)
import discord


# Local application imports
from discord_habit_tracker.models.message_event import MessageEvent


# =============================================================================
# Discord Gateway
# =============================================================================

class DiscordGateway:
    """
    Manages all communication between the application and Discord.

    This class owns the Discord client and is responsible for receiving
    events from Discord and forwarding them to the rest of the application.

    Main interface between Discord and the application.

    Think of this class as an adapter.

    Discord -> Gateway -> Application
    Application -> Gateway -> Discord
    """

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------


    def __init__(self, bot_token: str, message_handler):

        """

        Initialize the Discord Gateway.

        Responsibilities:

            - Configure gateway intents

            - Create the Discord client

            - Prepare the gateway for startup

        Does NOT:

            - Connect to Discord

            - Process events

            - Start the bot

        """

        # Bot token
        self._bot_token = bot_token


        # Store message handler
        self._message_handler = message_handler


        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True


        # Create Discord client
        self._client = discord.Client(intents=intents)

        self._client.event(self._on_message)


        # Store references to application services

    # -------------------------------------------------------------------------
    # Connection Lifecycle
    # -------------------------------------------------------------------------

    # Connect to Discord
    async def start(self):
        """Start the Discord Gateway."""

        await self._client.start(self._bot_token)

    # Disconnect gracefully

    # Handle startup

    # Handle shutdown

    # -------------------------------------------------------------------------
    # Discord Event Listeners
    # -------------------------------------------------------------------------

    # on_ready()

    # on_message()
    async def _on_message(self, message):

        """Handle an incoming Discord message."""

        event = MessageEvent(

            user_id=message.author.id,

            timestamp=message.created_at,

        )

        await self._message_handler(event)



    # on_error()

    # -------------------------------------------------------------------------
    # Outgoing Messages
    # -------------------------------------------------------------------------

    # Send log message

    # Send notification

    # Send embed

    # Future:
    # Send summary
    # Send leaderboard

# =============================================================================
# Internal Helper Functions
# =============================================================================

# Convert Discord objects into application objects

# Validate incoming data

# Utility functions



# =============================================================================
# Entry Point
# =============================================================================

# Create gateway

# Connect bot

# Handle shutdown signals
