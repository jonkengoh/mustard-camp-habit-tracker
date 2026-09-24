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
from discord_habit_tracker.models.activity_event import ActivityEvent


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

    def __init__(
        self,
        activity_repository,
        tracked_user_ids,
        activity_qualification_service,
        activity_date_resolver,
        tracked_user_timezone,
    ):
        """Initialize the Event Listener."""
        self._activity_repository = activity_repository
        self._tracked_user_ids = tracked_user_ids
        self._activity_qualification_service = activity_qualification_service
        self._activity_date_resolver = activity_date_resolver
        self._tracked_user_timezone = tracked_user_timezone

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------

    async def handle_message(self, event: MessageEvent):
        """Handle an incoming MessageEvent."""

        # Check if the event is from the tracked user
        if event.user_id not in self._tracked_user_ids:
            return

        # Check if the event qualifies as an activity
        qualifies = await self._activity_qualification_service.qualifies(event)

        if not qualifies:
            return

        # Resolve the activity date using the tracked user's timezone
        activity_date = self._activity_date_resolver.resolve(
            event.timestamp,
            self._tracked_user_timezone,
        )

        # Check if the user already has activity recorded for that date
        has_activity = await self._activity_repository.has_activity_for_date(
            event.guild_id,
            event.user_id,
            activity_date,
        )

        # If the user already has activity recorded for that date, do not record it again
        if has_activity:
            return

        # Create an ActivityEvent from the qualifying message
        activity = ActivityEvent(
            guild_id=event.guild_id,
            user_id=event.user_id,
            activity_date=activity_date,
        )

        # Forward the activity to the repository for recording
        await self._activity_repository.record(activity)
