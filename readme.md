# Personal Discord Habit & Activity Tracker

A production-quality Discord bot that automatically tracks daily activity and habit streaks.

> **Current Status:** 🚧 Phase 1 – Discord Gateway & Event Listener

---

## Architecture

The project is structured around separating Discord-specific communication from application logic and persistence.

```text
Discord
   ↓
DiscordGateway
   ↓
MessageEvent
   ↓
EventListener
   ↓
MessageRepository
   ↓
Storage (Planned)


## Components

Discord Gateway

Responsible for communicating with Discord and translating Discord events into application-level events.

* Connects to Discord
* Configures Discord intents
* Receives Discord messages
* Converts Discord messages into MessageEvent
* Forwards events to the application layer
* Contains no business logic

Event Listener

Responsible for application-level message processing and business logic.

* Receives MessageEvent
* Identifies the tracked user
* Determines whether an activity qualifies
* Handles first-message-of-the-day detection
* Passes qualifying events to the repository

Models

Shared application-level data structures.

* MessageEvent
    * user_id
    * timestamp

The model intentionally contains only the information required by the application rather than exposing Discord-specific objects.

Message Repository

Responsible for persistence-related operations.

* Records qualifying message events
* Provides queries required by the application
* Abstracts the underlying storage implementation

Storage technology has not yet been selected.

⸻

## Project Progress

### Phase 1 — Discord Gateway & Event Listener

#### 1. Project Setup

* Create project repository ✅
* Set up Python virtual environment ✅
* Install discord.py ✅
* Create .env file ✅
* Configure .gitignore ✅
* Verify project runs locally ✅
* Configure test environment with pytest ✅
* Add asynchronous testing support with pytest-asyncio ✅

#### 2. Discord Gateway

* Create DiscordGateway class ✅
* Configure Discord intents ✅
* Load bot token from configuration
* Connect to Discord
* Receive on_message events
* Translate Discord messages into MessageEvent ✅
* Forward events to the application layer ✅
* Keep Discord-specific logic isolated to the Gateway ✅

#### 3. Event Listener

* Create EventListener ✅
* Receive application-level MessageEvent objects ✅
* Filter messages by tracked user ✅
* Ignore untracked users ✅
* Pass qualifying events to the repository ✅
* Detect the first qualifying message of the day 🚧

#### 4. Repository

* Define MessageRepository interface ✅
* Record message events 🚧
* Query whether a user has activity for a given date 🚧
* Implement persistent storage ⏳

#### 5. Testing

* Test Event Listener behavior ✅
* Test tracked-user filtering ✅
* Test untracked-user filtering ✅
* Test repository interaction 🚧
* Test first-message-of-the-day detection ⏳
* Test Discord Gateway event translation ⏳

⸻

## Next Phase

After the Discord Gateway and Event Listener foundations are complete, planned features include:

* First Message Detection
* Activity Qualification Service
* Database Design
* Activity Repository
* Streak Engine
* Notification Service
* Multiple Users / Habits
* Configurable Channels
* Activity Statistics
* Heatmaps
* Leaderboards
* Achievements
* Web Dashboard

⸻

## Development Philosophy

The project is being developed incrementally with an emphasis on learning and maintainability.

Key principles include:

* Separation of concerns
* Dependency injection
* Test-driven development
* Asynchronous programming
* Clear application boundaries
* Discord-specific logic isolated from business logic
* Persistence isolated behind repository interfaces
* Small, incremental Git commits

⸻

## Testing

The project uses pytest and pytest-asyncio for automated testing.

Current test suite:

12 tests passing ✅

The test suite is expanded alongside new functionality to ensure existing behavior remains intact.

⸻

## Project Structure

```
discord-habit-tracker/
├── src/
│   └── discord_habit_tracker/
│       ├── models/
│       │   └── message_event.py
│       ├── repositories/
│       │   └── message_repository.py
│       ├── discord_gateway.py
│       └── event_listener.py
│
├── tests/
│   └── test_event_listener.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The project structure will evolve as additional components are introduced.

