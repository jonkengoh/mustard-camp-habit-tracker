# Personal Discord Habit Tracker Project

## Components (WIP)
1. Discord Gateway, Event listener (Listen for messages)


## Components (Planned)
1. Event Logger
2. Repository Database
3. Notification Service


# Discord Habit & Activity Tracker Bot

A production-quality Discord bot that automatically tracks daily activity and habit streaks.

Current Status: 🚧 Phase 1 – Discord Gateway & Event Listener

⸻

Phase 1 — Discord Gateway & Event Listener

1. Project Setup ✅

- Create project repository ✅
- Set up Python virtual environment ✅
- Install discord.py ✅
- Create .env file ✅
- Configure .gitignore ✅
- Verify project runs locally ✅

⸻

2. Discord Gateway

- Create DiscordGateway class
- Configure Discord Intents
- Load bot token from .env
- Connect to Discord
- Verify on_ready() is called
- Display bot information on startup

⸻

3. Event Listener

- Register on_message() event
- Ignore messages sent by bots
- Ignore system messages
- Print received message information to the console
- Confirm every qualifying message is detected

⸻

4. Code Quality

- Organize project structure
- Add module documentation
- Add logging
- Add type hints
- Refactor for readability

⸻

Next Phase

After the event listener is working, additional features would be:

- Activity Qualification Service
- First Message Detection
- Database Design
- Activity Repository
- Streak Engine
