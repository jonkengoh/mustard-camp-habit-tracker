import discord

from discord_habit_tracker.commands.discord_timezone_update_select import (
        TimezoneUpdateSelect,
    )

class TimezoneUpdateSelectView(discord.ui.View):
    """Discord view containing the timezone update selector."""

    def __init__(self, membership_service):
        super().__init__()
        self.add_item(TimezoneUpdateSelect(membership_service))
