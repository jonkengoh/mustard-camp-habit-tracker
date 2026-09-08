from datetime import date
from discord_habit_tracker.models.message_event import MessageEvent


class MessageRepository:
    def __init__(self):
        self._messages = set()

    async def record(self, event: MessageEvent):
        self._messages.add(
            (event.user_id, event.timestamp.date())
        )

    async def has_message_for_date(
        self,
        user_id: int,
        message_date: date,
    ) -> bool:
        return (user_id, message_date) in self._messages
