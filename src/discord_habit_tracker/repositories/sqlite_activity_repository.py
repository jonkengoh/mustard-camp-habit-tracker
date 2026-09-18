import sqlite3
from datetime import date

from discord_habit_tracker.models.activity_event import ActivityEvent


class SQLiteActivityRepository:
    """Stores and retrieves user activity using SQLite."""

    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                user_id INTEGER NOT NULL,
                activity_date TEXT NOT NULL,
                PRIMARY KEY (user_id, activity_date)
            )
            """
        )

        self._connection.commit()

    async def record(self, activity: ActivityEvent):
        """Record a user's activity."""

        self._connection.execute(
            """
            INSERT OR IGNORE INTO activities (user_id, activity_date)
            VALUES (?, ?)
            """,
            (
                activity.user_id,
                activity.activity_date.isoformat(),
            ),
        )

        self._connection.commit()

    async def has_activity_for_date(
        self,
        user_id: int,
        activity_date: date,
    ) -> bool:
        """Return whether the user has activity recorded for the date."""

        cursor = self._connection.execute(
            """
            SELECT 1
            FROM activities
            WHERE user_id = ? AND activity_date = ?
            """,
            (
                user_id,
                activity_date.isoformat(),
            ),
        )

        return cursor.fetchone() is not None

    async def get_activity_dates(self, user_id: int) -> set[date]:
        """Return all recorded activity dates for the user."""

        cursor = self._connection.execute(
            """
            SELECT activity_date
            FROM activities
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return {
            date.fromisoformat(row[0])
            for row in cursor.fetchall()
        }

    def close(self):
        """Close the database connection."""

        self._connection.close()
        self._connection = None
