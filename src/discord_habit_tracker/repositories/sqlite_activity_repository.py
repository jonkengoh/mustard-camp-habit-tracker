import sqlite3
from datetime import date

from discord_habit_tracker.models.activity_event import ActivityEvent


class SQLiteActivityRepository:
    """Stores and retrieves user activity using SQLite."""

    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)

        columns = self._connection.execute(
            "PRAGMA table_info(activities)"
        ).fetchall()

        if columns:
            column_names = {column[1] for column in columns}

            if "guild_id" not in column_names:
                self._connection.execute(
                    "DROP TABLE activities"
                )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                activity_date TEXT NOT NULL,
                PRIMARY KEY (guild_id, user_id, activity_date)
            )
            """
        )

        self._connection.commit()

    async def record(self, activity: ActivityEvent):
        """Record a user's activity."""

        self._connection.execute(
            """
            INSERT OR IGNORE INTO activities (
                guild_id,
                user_id,
                activity_date
            )
            VALUES (?, ?, ?)
            """,
            (
                activity.guild_id,
                activity.user_id,
                activity.activity_date.isoformat(),
            ),
        )

        self._connection.commit()

    async def has_activity_for_date(
        self,
        guild_id: int,
        user_id: int,
        activity_date: date,
    ) -> bool:
        """Return whether the user has activity recorded for the date."""

        cursor = self._connection.execute(
            """
            SELECT 1
            FROM activities
            WHERE guild_id = ? AND user_id = ? AND activity_date = ?
            """,
            (
                guild_id,
                user_id,
                activity_date.isoformat(),
            ),
        )

        return cursor.fetchone() is not None

    async def get_activity_dates(self, guild_id, user_id: int) -> set[date]:
        """Return all recorded activity dates for the user."""

        cursor = self._connection.execute(
            """
            SELECT activity_date
            FROM activities
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id),
        )

        return {
            date.fromisoformat(row[0])
            for row in cursor.fetchall()
        }

    def close(self):
        """Close the database connection."""

        self._connection.close()
        self._connection = None
