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
├── Define persistence behavior  ✅
├── SQLite schema                ✅
├── SQLite repository             ✅
├── Persistence tests             ✅
├── Application wiring            ✅
└── Restart/persistence test      ✅

PHASE 3 — Activity History
├── Query activity dates          ✅
├── Date-range history            ⬜
└── Basic activity statistics     ⬜

PHASE 4 — Streak Engine
├── Current streak                ✅
├── Longest streak                ✅
└── Edge cases around dates/timezones ✅

PHASE 5 — Activity Statistics
├── ActivityStatsService          ✅
├── Current streak coordination   ✅
└── Longest streak coordination   ✅

PHASE 6 — Discord Commands
├── !streak
├── !history
├── !stats
└── Possibly slash commands

PHASE 7 — Expansion
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
   ├── ActivityQualificationService
   ├── ActivityDateResolver
   └── ActivityRepository
           ↓
      ActivityEvent
           ↓
     SQLite Storage


ActivityRepository
        ↓
  Activity Dates
        ↓
ActivityStatsService
        ↓
   StreakService
   ├── Current Streak
   └── Longest Streak
```

The Discord gateway is responsible only for translating Discord-specific events into application-level events. The Event Listener coordinates application behavior, while domain services handle qualification, date resolution, and streak calculations.

Activity is persisted using SQLite. The repository abstracts storage operations from the rest of the application.

The statistics layer retrieves activity history through the repository and delegates streak calculations to the Streak Service.

This separation keeps Discord-specific details, application orchestration, business logic, and persistence independently testable.

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
* Resolves the message timestamp to the tracked user’s local calendar date
* Checks whether activity already exists for the event date
* Creates an ActivityEvent for qualifying activity
* Passes recorded activity to the repository

### Activity Qualification Service

Responsible for determining whether an incoming event qualifies as activity.

The current implementation uses a deliberately simple rule:

* Every tracked Discord message qualifies as activity

The service is isolated from the Event Listener so that qualification rules can evolve without coupling them to event handling or persistence.

### Activity Date Resolver

Responsible for converting a message timestamp into the tracked user’s local calendar date.

* Uses the configured IANA timezone
* Converts timestamps using Python’s zoneinfo
* Produces a calendar date for ActivityEvent
* Keeps timezone handling separate from event processing

This ensures that activity is recorded according to the user’s local day rather than the Discord server or system timezone.

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
* Retrieves recorded activity dates for a user
* Abstracts the underlying storage implementation

The project currently contains both an in-memory ActivityRepository implementation for lightweight testing and a SQLiteActivityRepository for persistent application storage.

### SQLite Activity Repository

Provides persistent storage using SQLite.

* Stores activity by user ID and calendar date
* Enforces one activity record per user per date
* Supports activity existence checks
* Retrieves activity dates
* Persists data across application restarts
* Handles database connection lifecycle

SQLite stores calendar dates using ISO-8601 YYYY-MM-DD strings.

### Streak Service

Responsible for calculating activity streaks from recorded activity dates.

* Calculates the current streak
* Calculates the longest streak
* Handles missing activity dates
* Handles empty activity history

The service contains streak calculation logic without depending on repositories or Discord.

### Activity Stats Service

Coordinates activity history retrieval and statistics calculation.

* Retrieves activity dates for a user
* Delegates current streak calculation to StreakService
* Delegates longest streak calculation to StreakService

This keeps repository access separate from the underlying streak calculation logic.

### Configuration

Responsible for loading and validating application configuration.

Current configuration includes:

* Discord bot token
* Tracked Discord user ID
* Tracked user timezone

Environment variables are loaded from .env, while .env.example documents the required configuration without containing real credentials.

### Application Entry Point

main.py acts as the composition root.

It:

* Creates the application configuration
* Creates the application data directory
* Creates the SQLite activity repository
* Creates the activity qualification service
* Creates the activity date resolver
* Creates the event listener
* Creates the Discord gateway
* Injects dependencies between components
* Starts the Discord gateway
* Closes the database connection when the application stops

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
* Retrieve activity dates for a user ✅
* Use in-memory storage for lightweight tests ✅
* Add SQLite persistence ✅
* Enforce one activity per user and calendar date ✅
* Test persistence across repository instances ✅
* Test database lifecycle and cleanup ✅

#### 7. Timezone-Aware Activity Dates

* Create ActivityDateResolver ✅
* Resolve timestamps using IANA timezones ✅
* Load tracked user timezone from configuration ✅
* Integrate date resolution into Event Listener ✅
* Test timezone-specific date boundaries ✅

#### 8. Application Wiring
* Create application composition root ✅
* Inject ActivityRepository into Event Listener ✅
* Inject ActivityQualificationService into Event Listener ✅
* Inject ActivityDateResolver into Event Listener ✅
* Inject Event Listener into Discord Gateway ✅
* Start the Gateway from the application entry point ✅
* Close the SQLite repository when the application stops ✅
* Test application dependency wiring ✅

### Phase 2 — Activity History & Statistics

#### 9. Activity History

* Add repository support for retrieving activity dates ✅
* Return activity dates for a specific user ✅
* Test activity date retrieval ✅
* Add date-range history queries ⬜

#### 10. Streak Engine

* Create StreakService ✅
* Calculate current streak ✅
* Calculate longest streak ✅
* Handle missing activity dates ✅
* Handle empty activity history ✅
* Test streak calculation behavior ✅

#### 11. Activity Statistics

* Create ActivityStatsService ✅
* Coordinate activity history retrieval ✅
* Coordinate current streak calculation ✅
* Coordinate longest streak calculation ✅
* Test statistics service coordination ✅

### Phase 3 — Discord Commands

* Add !streak ⬜
* Add !history ⬜
* Add !stats ⬜
* Consider slash commands ⬜

### Phase 4 — Expansion

* Multiple users ⬜
* Multiple habits ⬜
* Configurable qualification rules ⬜
* Notifications ⬜
* Statistics / heatmaps ⬜
* Achievements ⬜
* Web dashboard ⬜

## Next Phase

The next development milestone is to expose the application’s activity statistics through Discord.

Planned work includes:

* Discord command architecture
* Current streak command
* Longest streak command
* Activity history command
* Basic statistics command
* Command testing
* Keeping Discord command handling separate from application services

Additional functionality can be introduced as requirements emerge rather than adding abstractions prematurely.

## Development Philosophy

The project is being developed incrementally with an emphasis on learning and maintainability.

Key principles include:

* Separation of concerns
* Dependency injection
* Test-driven development
* Asynchronous programming
* Clear application boundaries
* Discord-specific logic isolated from business logic
* Persistence isolated behind repository implementations
* Small, incremental Git commits
* Avoiding unnecessary abstractions until requirements justify them

## Testing

The project uses pytest and pytest-asyncio for automated testing.

Current test suite: 47 tests passing ✅

Testing currently covers:

* Configuration loading and validation
* Discord Gateway initialization and startup
* Discord message translation
* Event Listener behavior
* Tracked-user filtering
* Activity qualification
* First-activity-of-the-day detection
* ActivityEvent behavior
* In-memory Activity Repository behavior
* SQLite Activity Repository behavior
* Activity persistence across repository instances
* Activity date retrieval
* Timezone-aware activity date resolution
* Application dependency wiring
* Integration between the Event Listener and Activity Repository
* Current streak calculation
* Longest streak calculation
* Activity statistics coordination

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
│       │   ├── activity_repository.py
│       │   └── sqlite_activity_repository.py
│       ├── services/
│       │   ├── activity_date_resolver.py
│       │   ├── activity_qualification_service.py
│       │   ├── activity_stats_service.py
│       │   └── streak_service.py
│       ├── config.py
│       ├── discord_gateway.py
│       ├── event_listener.py
│       └── main.py
│
├── tests/
│   ├── test_activity_date_resolver.py
│   ├── test_activity_event.py
│   ├── test_activity_qualification.py
│   ├── test_activity_repository.py
│   ├── test_activity_stats_service.py
│   ├── test_config.py
│   ├── test_discord_gateway.py
│   ├── test_event_listener.py
│   ├── test_main.py
│   ├── test_message_flow.py
│   ├── test_sqlite_activity_repository.py
│   └── test_streak_service.py
│
├── data/
│   └── activity_tracker.db
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The project structure will evolve as additional components are introduced.

