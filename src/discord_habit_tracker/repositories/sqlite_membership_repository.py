import sqlite3


class SQLiteMembershipRepository:
    """Stores tracker membership using SQLite."""

    def __init__(self, database_path: str):
        self._connection = sqlite3.connect(database_path)

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        self._connection.commit()

    async def add_member(self, guild_id: int, user_id: int):
        """Add a user as a tracker member."""

        self._connection.execute(
            """
            INSERT OR IGNORE INTO members (
                guild_id,
                user_id
            )
            VALUES (?, ?)
            """,
            (guild_id, user_id),
        )

        self._connection.commit()

    async def is_member(self, guild_id: int, user_id: int) -> bool:
        """Return whether a user is a tracker member."""

        cursor = self._connection.execute(
            """
            SELECT 1
            FROM members
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id),
        )

        return cursor.fetchone() is not None


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
