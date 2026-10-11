from discord_habit_tracker.models.tracker_member import TrackerMember


def test_tracker_member_stores_membership_details():
    """Test that a tracker member stores guild, user, and timezone."""

    member = TrackerMember(
        guild_id=999,
        user_id=12345,
        timezone="Asia/Singapore",
    )

    assert member.guild_id == 999
    assert member.user_id == 12345
    assert member.timezone == "Asia/Singapore"
