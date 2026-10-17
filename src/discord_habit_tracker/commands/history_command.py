from datetime import date, timedelta


class HistoryCommand:
    """Handles activity history queries."""

    def __init__(self, activity_repository):
        self._activity_repository = activity_repository

    async def handle(
        self,
        guild_id: int,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> str:
        """Return formatted activity history for a date range."""

        if start_date > end_date:
            raise ValueError("start_date must be on or before end_date")

        activity_dates = (
            await self._activity_repository.get_activity_dates_in_range(
                guild_id,
                user_id,
                start_date,
                end_date,
            )
        )

        total_days = (end_date - start_date).days + 1
        active_days = len(activity_dates)
        activity_rate = active_days / total_days * 100

        if start_date == end_date:
            period = start_date.strftime("%d %b %Y").lstrip("0")
        else:
            period = (
                f"{start_date.strftime('%d %b').lstrip('0')} – "
                f"{end_date.strftime('%d %b %Y').lstrip('0')}"
            )

        lines = [f"Activity History ({period})"]

        if not activity_dates:
            lines.append("No activity recorded during this period.")
        else:
            current_date = end_date

            while current_date >= start_date:
                if current_date in activity_dates:
                    marker = "✓"
                else:
                    marker = "✗"

                lines.append(
                    f"{marker} {current_date.strftime('%a, %d %b').lstrip('0')}"
                )

                current_date -= timedelta(days=1)

        lines.extend([
            "",
            f"Active days: {active_days}/{total_days} "
            f"({activity_rate:.1f}%)",
        ])

        return "\n".join(lines)
