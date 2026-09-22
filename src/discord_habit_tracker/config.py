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

        tracked_user_ids = os.getenv("DISCORD_TRACKED_USER_IDS")

        if not tracked_user_ids:
            raise ValueError("DISCORD_TRACKED_USER_IDS is not configured.")

        try:
            self.tracked_user_ids = {
                int(user_id.strip())
                for user_id in tracked_user_ids.split(",")
            }
        except ValueError as exc:
            raise ValueError(
                "DISCORD_TRACKED_USER_IDS must contain valid integers."
            ) from exc

        tracked_user_timezone = os.getenv("DISCORD_TRACKED_USER_TIMEZONE")
        if not tracked_user_timezone:
            raise ValueError(
                "DISCORD_TRACKED_USER_TIMEZONE is not configured."
            )

        self.tracked_user_timezone = tracked_user_timezone
