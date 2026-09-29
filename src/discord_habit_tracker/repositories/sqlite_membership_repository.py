import sqlite3

from discord_habit_tracker.models.tracker_member import TrackerMember


class SQLiteMembershipRepository:
    """Stores tracker membership using SQLite."""

    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                timezone TEXT NOT NULL,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        self._connection.commit()

    async def add_member(self, guild_id: int, user_id: int, timezone: str):
        """Add a user as a tracker member."""

        self._connection.execute(
            """
            INSERT OR IGNORE INTO members (
                guild_id,
                user_id,
                timezone
            )
            VALUES (?, ?, ?)
            """,
            (guild_id, user_id, timezone),
        )

        self._connection.commit()

    async def get_member(self, guild_id: int, user_id: int) -> TrackerMember | None:
        """Return a tracker member if they exist."""

        cursor = self._connection.execute(
            """
            SELECT guild_id, user_id, timezone
            FROM members
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return TrackerMember(
            guild_id=row[0],
            user_id=row[1],
            timezone=row[2],
        )


    async def remove_member(self, guild_id: int, user_id: int):
        """Remove a user from tracker membership."""

        self._connection.execute(
            """
            DELETE FROM members
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id),
        )

        self._connection.commit()


    def close(self):
        """Close the database connection."""

        self._connection.close()
        self._connection = None
