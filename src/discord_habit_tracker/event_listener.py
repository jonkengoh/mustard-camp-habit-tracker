"""
event_listener.py

Purpose:
    Handles application events received from external sources.

Responsibilities:
    - Receive application events
    - Process incoming events
    - Coordinate application logic

Non-Responsibilities:
    - Discord communication
    - Database implementation
    - Discord-specific data handling

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


# Local application imports
from discord_habit_tracker.models.message_event import MessageEvent


# =============================================================================
# Event Listener
# =============================================================================

class EventListener:
    """
    Handles application events.

    Receives application-level events from the Discord Gateway and
    coordinates their processing.

    Discord-specific objects should not enter this layer.
    """

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    def __init__(self, message_repository, tracked_user_id):
        """Initialize the Event Listener."""

        self._message_repository = message_repository
        self._tracked_user_id = tracked_user_id

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------

    async def handle_message(self, event: MessageEvent):
        """Handle an incoming MessageEvent."""

        # Check if the event is from the tracked user
        if event.user_id != self._tracked_user_id:
            return


        # Check if the user already has a message recorded for that date
        has_message = await self._message_repository.has_message_for_date(
            event.user_id,
            event.timestamp.date(),
        )

        # If the user already has a message for that date, do not record it again
        if has_message:
            return

        # Forward the event to the repository for recording
        await self._message_repository.record(event)




