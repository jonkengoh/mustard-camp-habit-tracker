from datetime import date, timedelta


class StreakService:
    """Calculates user activity streaks."""

    def calculate_current_streak(
        self,
        activity_dates: set[date],
        current_date: date,
    ) -> int:
        """Return the number of consecutive activity days ending today."""

        streak = 0
        date_to_check = current_date

        while date_to_check in activity_dates:
            streak += 1
            date_to_check -= timedelta(days=1)

        return streak

    def calculate_longest_streak(
        self,
        activity_dates: set[date],
    ) -> int:
        """Return the longest sequence of consecutive activity dates."""

        if not activity_dates:
            return 0

        longest_streak = 0

        for activity_date in activity_dates:
            streak = 1
            date_to_check = activity_date + timedelta(days=1)

            while date_to_check in activity_dates:
                streak += 1
                date_to_check += timedelta(days=1)

            longest_streak = max(longest_streak, streak)

        return longest_streak


