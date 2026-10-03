from unittest.mock import Mock

from discord_habit_tracker.commands.discord_timezone_select import (
    TimezoneSelect,
)
from discord_habit_tracker.commands.timezone_select_view import (
    TimezoneSelectView,
)


def test_timezone_select_view_contains_timezone_select():
    membership_service = Mock()
    view = TimezoneSelectView(membership_service)

    assert len(view.children) == 1
    assert isinstance(view.children[0], TimezoneSelect)
