from discord_habit_tracker.models.message_event import MessageEvent


class MessageRepository:
    async def record(self, event: MessageEvent):
        ...

