from dataclasses import dataclass
from datetime import datetime


@dataclass
class MessageEvent:
    """Represents a message event within the application."""

    user_id: int
    timestamp: datetime
