# Personal Discord Habit & Activity Tracker

A production-quality Discord bot that automatically tracks daily activity and habit streaks.

> **Current Status:** 🚧 Phase 1 – Core Event Pipeline Complete; Activity Qualification Next

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
```

The current implementation uses in-memory storage. Persistent storage will be introduced in a later phase.

## Components

#### Discord Gateway

Responsible for communicating with Discord and translating Discord events into application-level events.

* Connects to Discord
* Configures Discord intents
* Receives Discord messages
* Converts Discord messages into MessageEvent
* Forwards events to the application layer
* Contains no business logic

#### Event Listener

Responsible for application-level message processing and business logic.

* Receives MessageEvent
* Identifies the tracked user
* Determines whether an activity qualifies
* Handles first-message-of-the-day detection
* Passes qualifying events to the repository

#### Models

Shared application-level data structures.

* MessageEvent
    * user_id
    * timestamp

The model intentionally contains only the information required by the application rather than exposing Discord-specific objects.

#### Message Repository

Responsible for persistence-related operations.

* Records message events
* Checks whether a user has activity recorded for a given date
* Abstracts the underlying storage implementation

The current implementation uses an in-memory set. Persistent storage technology has not yet been selected.

#### Configuration

Responsible for loading and validating application configuration.

Current configuration includes:

* Discord bot token
* Tracked Discord user ID

Environment variables are loaded from .env, while .env.example documents the required configuration without containing real credentials.

#### Application Entry Point

main.py acts as the composition root.

It:

* Creates the application configuration
* Creates the repository
* Creates the event listener
* Creates the Discord gateway
* Injects dependencies between components
* Starts the Discord gateway

This keeps dependency wiring separate from application logic.

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

#### 3. Discord Gateway

* Create DiscordGateway class ✅
* Configure Discord intents ✅
* Load bot token from configuration ✅
* Start the Discord client ✅
* Register on_message handler ✅
* Translate Discord messages into MessageEvent ✅
* Forward events to the application layer ✅
* Keep Discord-specific logic isolated to the Gateway ✅

#### 4. Event Listener

* Create EventListener ✅
* Receive application-level MessageEvent objects ✅
* Filter messages by tracked user ✅
* Ignore untracked users ✅
* Check whether activity already exists for the event date ✅
* Record the first qualifying message of the day ✅


#### 5. Repository

* Create MessageRepository ✅
* Record message events ✅
* Query whether a user has activity for a given date ✅
* Use in-memory storage as the initial implementation ✅
* Implement persistent storage ⏳

#### 6. Application Wiring
* Create application composition root ✅
* Inject repository into Event Listener ✅
* Inject Event Listener into Discord Gateway ✅
* Start the Gateway from the application entry point ✅
* Test dependency wiring ✅

#### 7. Testing

* Test Event Listener behavior ✅
* Test tracked-user filtering ✅
* Test untracked-user filtering ✅
* Test existing-activity detection ✅
* Test first-message-of-the-day behavior ✅
* Test repository recording ✅
* Test repository date isolation ✅
* Test Discord Gateway initialization ✅
* Test Discord Gateway intents ✅
* Test Discord Gateway startup ✅
* Test Discord message → MessageEvent translation ✅
* Test application dependency wiring ✅
* Test real Event Listener → Repository message flow ✅

⸻

## Next Phase

The next development milestone is to make the concept of “activity” an explicit application-level concept rather than treating every tracked-user message as qualifying activity.

Planned work includes:

* Activity Qualification Service
* Explicit activity qualification rules
* Activity model / domain representation
* Activity Repository
* Persistent database design
* SQLite or other storage implementation
* Streak Engine
* Notification Service
* Multiple Users / Habits
* Configurable Channels
* Activity Statistics
* Heatmaps
* Leaderboards
* Achievements
* Web Dashboard

The architecture will continue to evolve as these requirements are introduced.

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

Current test suite: 21 tests passing ✅

Testing currently covers:

* Configuration loading and validation
* Discord Gateway initialization and startup
* Discord message translation
* Event Listener behavior
* Tracked-user filtering
* First-message-of-the-day detection
* Repository behavior
* Application dependency wiring
* Integration between the Event Listener and Message Repository

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
│       ├── config.py
│       ├── discord_gateway.py
│       ├── event_listener.py
│       └── main.py
│
├── tests/
│   ├── test_config.py
│   ├── test_discord_gateway.py
│   ├── test_event_listener.py
│   ├── test_main.py
│   ├── test_message_flow.py
│   └── test_repository.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The project structure will evolve as additional components are introduced.

