# Personal Discord Habit & Activity Tracker

A production-quality Discord bot that automatically tracks daily activity and habit streaks.

> **Current Status:** 🚧 Phase 1 – Core Activity Pipeline Complete

## Project Roadmap
```
PHASE 1 — Core Activity Pipeline
├── Discord Gateway              ✅
├── MessageEvent                 ✅
├── EventListener                ✅
├── ActivityQualificationService ✅
├── ActivityEvent                ✅
├── ActivityRepository            ✅
├── Application wiring            ✅
└── Tests                         ✅

PHASE 2 — Persistent Activity
├── Define persistence behavior
├── SQLite schema
├── SQLite repository
├── Persistence tests
├── Application wiring
└── Restart/persistence test

PHASE 3 — Activity History
├── Query activity dates
├── Date-range history
└── Basic activity statistics

PHASE 4 — Streak Engine
├── Current streak
├── Longest streak
└── Edge cases around dates/timezones

PHASE 5 — Discord Commands
├── !streak
├── !history
├── !stats
└── Possibly slash commands

PHASE 6 — Expansion
├── Multiple users
├── Multiple habits
├── Configurable qualification rules
├── Notifications
├── Statistics/heatmaps
└── Web dashboard
```
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
ActivityQualificationService
   ↓
ActivityEvent
   ↓
ActivityRepository
   ↓
Storage (In-Memory)
```

The current implementation uses in-memory storage. Persistent storage will be introduced in a later phase.

The architecture intentionally separates the incoming Discord event from the application’s domain representation:

* MessageEvent represents an incoming Discord message.
* ActivityQualificationService determines whether the event qualifies as activity.
* ActivityEvent represents the resulting domain-level activity.
* ActivityRepository handles persistence of recorded activity.

This keeps Discord-specific details separate from application and persistence logic.

## Components

### Discord Gateway

Responsible for communicating with Discord and translating Discord events into application-level events.

* Connects to Discord
* Configures Discord intents
* Receives Discord messages
* Converts Discord messages into MessageEvent
* Forwards events to the application layer
* Contains no business logic

### Event Listener

Responsible for orchestrating application-level event processing.

* Receives MessageEvent
* Identifies the tracked user
* Passes events to the activity qualification service
* Checks whether activity already exists for the event date
* Creates an ActivityEvent for qualifying activity
* Passes recorded activity to the repository

### Activity Qualification Service

Responsible for determining whether an incoming event qualifies as activity.

The current implementation uses a deliberately simple rule:

* Every tracked Discord message qualifies as activity

The service is isolated from the Event Listener so that qualification rules can evolve without coupling them to event handling or persistence.

### Models

Shared application-level data structures.

* MessageEvent
    * user_id
    * timestamp
* ActivityEvent
    * user_id
    * activity_date

MessageEvent represents the incoming event from Discord, while ActivityEvent represents the application’s domain-level record of user activity.

### Activity Repository

Responsible for persistence-related operations.

* Records ActivityEvent instances
* Checks whether a user has activity recorded for a given date
* Abstracts the underlying storage implementation

The current implementation uses an in-memory set. Persistent storage technology has not yet been selected.

### Configuration

Responsible for loading and validating application configuration.

Current configuration includes:

* Discord bot token
* Tracked Discord user ID

Environment variables are loaded from .env, while .env.example documents the required configuration without containing real credentials.

### Application Entry Point

main.py acts as the composition root.

It:

* Creates the application configuration
* Creates the activity repository
* Creates the activity qualification service
* Creates the event listener
* Creates the Discord gateway
* Injects dependencies between components
* Starts the Discord gateway

This keeps dependency wiring separate from application logic.



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
* Load bot token from configuration ✅
* Start the Discord client ✅
* Register on_message handler ✅
* Translate Discord messages into MessageEvent ✅
* Forward events to the application layer ✅
* Keep Discord-specific logic isolated to the Gateway ✅

#### 3. Event Listener

* Create EventListener ✅
* Receive application-level MessageEvent objects ✅
* Filter messages by tracked user ✅
* Ignore untracked users ✅
* Delegate activity qualification ✅
* Check whether activity already exists for the event date ✅
* Convert qualifying messages into ActivityEvent objects ✅
* Record the first qualifying activity of the day ✅

#### 4. Activity Qualification

* Create ActivityQualificationService ✅
* Integrate qualification service with Event Listener ✅
* Add tests for activity qualification ✅
* Add tests for non-qualifying activity behavior ✅
* Keep qualification logic isolated from event handling and persistence ✅

#### 5. Activity Domain Model

* Create ActivityEvent ✅
* Represent activity using user ID and calendar date ✅
* Separate domain activity from Discord message details ✅
* Add ActivityEvent tests ✅

#### 6. Activity Repository

* Create ActivityRepository ✅
* Record ActivityEvent instances ✅
* Query whether a user has activity for a given date ✅
* Use in-memory storage as the initial implementation ✅
* Implement persistent storage ⏳

#### 7. Application Wiring
* Create application composition root ✅
* Inject ActivityRepository into Event Listener ✅
* Inject ActivityQualificationService into Event Listener ✅
* Inject Event Listener into Discord Gateway ✅
* Start the Gateway from the application entry point ✅
* Test application dependency wiring ✅

#### 8. Testing

* Test configuration loading and validation ✅
* Test Discord Gateway initialization ✅
* Test Discord Gateway intents ✅
* Test Discord Gateway startup ✅
* Test Discord message → MessageEvent translation ✅
* Test Event Listener behavior ✅
* Test tracked-user filtering ✅
* Test untracked-user filtering ✅
* Test activity qualification ✅
* Test existing-activity detection ✅
* Test first-activity-of-the-day behavior ✅
* Test ActivityEvent construction ✅
* Test Activity Repository recording ✅
* Test Activity Repository date isolation ✅
* Test Activity Repository user isolation ✅
* Test application dependency wiring ✅
* Test Event Listener → Activity Repository integration ✅



## Next Phase

The next development milestone is to introduce persistent storage and begin deriving useful streak information from recorded activity.

Planned work includes:

* Persistent database design
* SQLite or other storage implementation
* Repository persistence tests
* Streak Engine
* Current streak calculation
* Longest streak calculation
* Activity history queries
* Discord commands for streak/status/history
* Multiple Users / Habits
* Configurable activity rules
* Activity Statistics
* Heatmaps
* Leaderboards
* Achievements
* Notification Service
* Web Dashboard

The architecture will continue to evolve as additional requirements are introduced.



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
* Avoiding unnecessary abstractions until requirements justify them



## Testing

The project uses pytest and pytest-asyncio for automated testing.

Current test suite: 26 tests passing ✅

Testing currently covers:

Testing currently covers:

* Configuration loading and validation
* Discord Gateway initialization and startup
* Discord message translation
* Event Listener behavior
* Tracked-user filtering
* Activity qualification
* First-activity-of-the-day detection
* ActivityEvent behavior
* Activity Repository behavior
* Date and user isolation
* Application dependency wiring
* Integration between the Event Listener and Activity Repository

The test suite is expanded alongside new functionality to ensure existing behavior remains intact.



## Project Structure

```
discord-habit-tracker/
├── src/
│   └── discord_habit_tracker/
│       ├── models/
│       │   ├── activity_event.py
│       │   └── message_event.py
│       ├── repositories/
│       │   └── activity_repository.py
│       ├── services/
│       │   └── activity_qualification_service.py
│       ├── config.py
│       ├── discord_gateway.py
│       ├── event_listener.py
│       └── main.py
│
├── tests/
│   ├── test_activity_event.py
│   ├── test_activity_repository.py
│   ├── test_config.py
│   ├── test_discord_gateway.py
│   ├── test_event_listener.py
│   ├── test_main.py
│   ├── test_message_flow.py
│   └── test_activity_qualification.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The project structure will evolve as additional components are introduced.

