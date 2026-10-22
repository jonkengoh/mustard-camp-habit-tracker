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
                reminders_enabled INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        cursor = self._connection.execute("PRAGMA table_info(members)")
        columns = {row[1] for row in cursor.fetchall()}

        if "reminders_enabled" not in columns:
            self._connection.execute(
                """
                ALTER TABLE members
                ADD COLUMN reminders_enabled INTEGER NOT NULL DEFAULT 0
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
            SELECT guild_id, user_id, timezone, reminders_enabled
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
            reminders_enabled=bool(row[3]),
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


    async def update_timezone(
        self,
        guild_id: int,
        user_id: int,
        timezone: str,
    ):
        self._connection.execute(
            """
            UPDATE members
            SET timezone = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (timezone, guild_id, user_id),
        )
        self._connection.commit()


    async def set_reminders_enabled(
        self,
        guild_id: int,
        user_id: int,
        enabled: bool,
    ) -> None:
        """Update whether a member has opted into daily reminders."""

        self._connection.execute(
            """
            UPDATE members
            SET reminders_enabled = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (int(enabled), guild_id, user_id),
        )
        self._connection.commit()


    async def get_members_with_reminders_enabled(
        self,
    ) -> list[TrackerMember]:
        """Return all members who have opted into daily reminders."""

        cursor = self._connection.execute(
            """
            SELECT guild_id, user_id, timezone, reminders_enabled
            FROM members
            WHERE reminders_enabled = 1
            """
        )

        return [
            TrackerMember(
                guild_id=row[0],
                user_id=row[1],
                timezone=row[2],
                reminders_enabled=bool(row[3]),
            )
            for row in cursor.fetchall()
        ]


    def close(self):
        """Close the database connection."""

        self._connection.close()
        self._connection = None
