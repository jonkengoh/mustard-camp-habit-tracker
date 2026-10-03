import discord

from discord_habit_tracker.commands.discord_timezone_select import (
    TimezoneSelect,
)


class TimezoneSelectView(discord.ui.View):
    """Discord view containing the timezone selector."""

    def __init__(self, membership_service):
        super().__init__()

        self.add_item(TimezoneSelect(membership_service))
