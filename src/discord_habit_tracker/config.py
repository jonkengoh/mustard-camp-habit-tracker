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

        tracked_user_timezone = os.getenv("DISCORD_TRACKED_USER_TIMEZONE")
        if not tracked_user_timezone:
            raise ValueError(
                "DISCORD_TRACKED_USER_TIMEZONE is not configured."
            )

        self.tracked_user_timezone = tracked_user_timezone
