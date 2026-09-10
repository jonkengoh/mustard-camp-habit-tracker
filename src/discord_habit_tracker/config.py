"""
Application configuration.

Loads and validates configuration required by the application.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Stores application configuration."""

    def __init__(self):
        bot_token = os.getenv("DISCORD_TOKEN")

        if not bot_token:
            raise ValueError("DISCORD_TOKEN is not configured.")

        self.bot_token = bot_token

        tracked_user_id = os.getenv("DISCORD_TRACKED_USER_ID")

        if not tracked_user_id:
            raise ValueError("DISCORD_TRACKED_USER_ID is not configured.")

        try:
            self.tracked_user_id = int(tracked_user_id)
        except ValueError as exc:
            raise ValueError(
                "DISCORD_TRACKED_USER_ID must be a valid integer."
            ) from exc
