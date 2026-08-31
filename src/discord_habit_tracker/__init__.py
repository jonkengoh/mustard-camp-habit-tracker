def __init__(self, bot_token: str, message_handler):
    """Initialize the Discord Gateway."""

    self._bot_token = bot_token
    self._message_handler = message_handler

    intents = discord.Intents.default()
    intents.message_content = True

    self._client = discord.Client(intents=intents)

