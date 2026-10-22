import sqlite3


class SQLiteReminderDeliveryRepository:
    """Stores records of successfully delivered daily reminders."""

    def __init__(self, database_path: str):
        """Initialize the repository and create its table if necessary."""

        self._connection = sqlite3.connect(database_path)

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reminder_deliveries (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                reminder_date TEXT NOT NULL,
                PRIMARY KEY (guild_id, user_id, reminder_date)
            )
            """
        )
        self._connection.commit()

    async def record_delivery(
        self,
        guild_id: int,
        user_id: int,
        reminder_date: str,
    ) -> None:
        """Record a successfully delivered reminder."""

        self._connection.execute(
            """
            INSERT INTO reminder_deliveries (
                guild_id,
                user_id,
                reminder_date
            )
            VALUES (?, ?, ?)
            ON CONFLICT (guild_id, user_id, reminder_date) DO NOTHING
            """,
            (guild_id, user_id, reminder_date),
        )
        self._connection.commit()

    async def has_delivery(
        self,
        guild_id: int,
        user_id: int,
        reminder_date: str,
    ) -> bool:
        """Return whether a delivery has already been recorded."""

        cursor = self._connection.execute(
            """
            SELECT 1
            FROM reminder_deliveries
            WHERE guild_id = ?
              AND user_id = ?
              AND reminder_date = ?
            """,
            (guild_id, user_id, reminder_date),
        )

        return cursor.fetchone() is not None

    def close(self) -> None:
        """Close the database connection."""

        self._connection.close()
