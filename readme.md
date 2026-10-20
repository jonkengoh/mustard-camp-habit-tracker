# Personal Discord Habit & Activity Tracker

A production-quality Discord bot that automatically tracks daily activity and habit streaks.

> **Current Status:** ✅ Phase 7 — Activity History & Statistics Complete · 🚧 Phase 8 — Daily Streak Reminders In Progress

## Project Roadmap
```
PHASE 1 — Core Activity Pipeline
├── ✅ Discord Gateway
├── ✅ MessageEvent
├── ✅ EventListener
├── ✅ ActivityQualificationService
├── ✅ ActivityEvent
├── ✅ ActivityRepository
├── ✅ Application wiring
└── ✅ Tests

PHASE 2 — Persistent Activity & Streaks
├── ✅ SQLite activity schema
├── ✅ SQLite activity repository
├── ✅ Persistence tests
├── ✅ Activity date retrieval
├── ✅ Timezone-aware dates
├── ✅ Current streak
├── ✅ Longest streak
├── ✅ ActivityStatsService
└── ✅ Application wiring

PHASE 3 — Discord Commands
├── ✅ StreakCommand
├── ✅ Discord streak command adapter
├── ✅ CurrentDateResolver
├── ✅ Slash command registration
├── ✅ Slash command synchronization
├── ✅ Live /streak verification
└── ✅ Discord activity tracking

PHASE 4 — Guild-Scoped Tracking
├── ✅ Guild context in application events
├── ✅ Guild-scoped activity persistence
├── ✅ Guild-scoped streak statistics
├── ✅ Multiple users per guild
├── ✅ Guild membership repository
├── ✅ Membership-based activity filtering
└── ✅ Remove global tracked-user config

PHASE 5 — Membership Management
├── ✅ Persistent SQLite membership storage
├── ✅ /streak join
├── ✅ /streak leave
├── ✅ /streak timezone
├── ✅ Membership command testing
├── ✅ Membership lifecycle handling
├── ✅ Timezone update persistence
└── ✅ Live Discord command verification

PHASE 6 — Activity Logging
├── ✅ #daily-streak channel logging
├── ✅ Automatic channel creation
└── ✅ Guild-scoped activity notifications

PHASE 7 — Activity History & Statistics
├── ✅ Date-range activity queries
├── ✅ /history command
├── ✅ Current and longest streak statistics
├── ✅ Recent activity count and rate
└── ✅ One-day current-streak grace period

PHASE 8 — Daily Streak Reminders
├── ⬜ Reminder opt-in and opt-out
├── ⬜ Configurable reminder channel
├── ⬜ Timezone-aware daily scheduling
├── ⬜ Remind eligible users with an active streak
├── ⬜ Avoid duplicate reminders per local calendar day
├── ⬜ Handle bot downtime and missed reminders
└── ⬜ Test scheduling, persistence, and delivery

FUTURE EXPANSION
├── ⬜ Multiple habits
├── ⬜ Configurable activity qualification rules
├── ⬜ Statistics and heatmaps
├── ⬜ Achievements
└── ⬜ Web dashboard
```

## Overview

The Personal Discord Habit & Activity Tracker is a Discord bot that records daily activity, calculates activity streaks, and provides activity history and statistics for participating members.

The project began as a single-user tracker and has evolved into a guild-scoped, multi-user activity tracking system.

Each Discord server maintains its own tracker membership and activity history. A user’s activity and streak in one server are independent of their activity and streak in another server.

Members can configure their own timezones, allowing activity dates and streak calculations to follow their local calendar days.

The current activity rule is intentionally simple:

* Any message sent by a tracker member qualifies as activity.
* Only the first qualifying message from a member on a given local calendar day is recorded.
* Newly recorded daily activity is announced in the guild’s #daily-streak channel.

The bot provides current and longest streak statistics through `/streak`, as well as date-range activity history and activity rates through `/history`.

The project is developed incrementally, with an emphasis on clean architecture, testability, dependency injection, and small, focused changes.


## Architecture

The project is structured around separating Discord-specific communication from application logic and persistence.

```text
Discord
   │
   ▼
DiscordGateway
   │
   ▼
MessageEvent
   │
   ▼
EventListener
   │
   ├── MembershipRepository
   │       │
   │       └── Is user a member of this guild?
   │
   ├── ActivityQualificationService
   │
   └── ActivityDateResolver
           │
           ▼
      ActivityEvent
           │
           ▼
   ActivityRepository
           │
           ▼
      SQLite Storage
```

The Discord gateway translates Discord-specific events into application-level events. The Event Listener coordinates activity processing, while domain services handle activity qualification, date resolution, and streak calculations.

Activity and membership data are persisted using SQLite. Repository interfaces abstract storage operations from the rest of the application, allowing in-memory implementations to be used for lightweight tests.

The statistics layer retrieves activity history through the activity repository and delegates streak calculations to the Streak Service. Application-level command handlers implement command behavior independently of Discord, while Discord slash-command adapters handle interactions and responses.

Activity notifications are handled by DiscordActivityNotifier, which manages the guild’s #daily-streak channel and formats announcements when new daily activity is recorded.

This separation keeps Discord-specific communication, application orchestration, business logic, and persistence independently testable.

## Streak Flow

```
Discord /streak
       │
       ▼
DiscordStreakSlashCommand
       │
       ▼
StreakCommand
       │
       ▼
ActivityStatsService
       │
       ├── Current streak
       │
       └── Longest streak
              │
              ▼
        StreakService
              │
              ▼
   ActivityRepository
```

The Discord command adapter handles Discord interaction details while StreakCommand, ActivityStatsService, and StreakService remain independent of Discord.

## Activity Notification Flow

When a message results in a newly recorded ActivityEvent, the Discord gateway retrieves the user’s updated streak through ActivityStatsService and delegates the announcement to DiscordActivityNotifier.

```
Discord Message
       |
       v
DiscordGateway
       |
       v
EventListener
       |
       v
New ActivityEvent?
       |
       v
ActivityStatsService
       |
       v
DiscordActivityNotifier
       |
       v
#daily-streak
```

Notifications are sent only when the event listener reports newly recorded activity. Messages that do not produce a new activity record do not trigger notifications.

DiscordActivityNotifier handles finding or creating the guild’s activity channel and formatting the notification. The gateway coordinates the flow without implementing the notification formatting itself.


## Guild Scoping

Activity and membership are scoped by both:

```text
guild_id
user_id
```

This means the same Discord user can participate independently in different servers.

For example:
```text
Guild A
├── User 12345 → activity tracked
└── User 67890 → activity tracked

Guild B
└── User 12345 → activity tracked independently
```

A user’s activity in Guild A does not affect their streak in Guild B.


## Components

### Discord Gateway

Responsible for communicating with Discord and translating Discord events into application-level events.

* Connects to Discord
* Configures required Discord intents
* Receives Discord messages
* Converts Discord messages into MessageEvent
* Forwards events to the application layer
* Registers Discord application commands
* Synchronizes application commands with Discord
* Contains no activity or streak business logic

### Event Listener

Responsible for orchestrating application-level event processing.

* Receives MessageEvent
* Checks guild membership
* Delegates activity qualification
* Resolves the message timestamp to the configured local calendar date
* Checks whether activity already exists for the date
* Creates an ActivityEvent
* Records qualifying activity through the repository


The Event Listener does not determine membership itself. Membership is provided through the MembershipRepository.

### Membership Repository

Responsible for tracker membership and member timezone preferences.

Membership is scoped to a Discord guild and user:

(guild_id, user_id)

The application provides both in-memory and SQLite-backed membership repositories.

It supports:

* Adding a user to a guild’s tracker
* Checking whether a user is a member
* Removing a user from a guild’s tracker
* Updating a member’s configured timezone
* Isolating membership between guilds
* Isolating membership between users
* Persisting membership and timezone preferences across application restarts

The membership service coordinates membership operations and validates timezone selections before updating stored preferences.

Discord slash-command adapters expose membership operations through /streak join, /streak leave, and /streak timezone.

### Activity Qualification Service

Responsible for determining whether an incoming event qualifies as activity.

The current implementation uses a deliberately simple rule:

* Every tracked Discord message qualifies as activity

The service is isolated from the Event Listener so that qualification rules can evolve without coupling them to event handling or persistence.

### Activity Date Resolver

Responsible for converting message timestamps into local calendar dates.

* Uses the configured IANA timezone
* Uses Python’s zoneinfo
* Produces a calendar date for ActivityEvent
* Keeps timezone handling separate from event processing

This ensures activity is recorded according to the configured local day rather than the Discord server or machine timezone.

### Current Date Resolver

Responsible for resolving the current calendar date in the configured timezone.

* Uses the configured IANA timezone
* Obtains the current timezone-aware timestamp
* Produces the local calendar date
* Keeps current-date resolution separate from Discord command handling

This allows commands such as ```/streak``` to calculate streaks according to the configured member’s local day rather than the machine’s local timezone.

### Models

Shared application-level data structures.

#### MessageEvent
Represents an incoming Discord message:
```text
guild_id
user_id
timestamp
```

#### ActivityEvent
Represents recorded activity:
```text
guild_id
user_id
activity_date
```

Separating ```MessageEvent``` from ```ActivityEvent``` prevents Discord-specific message details from leaking into the activity domain.

MessageEvent represents the incoming event from Discord, while ActivityEvent represents the application’s domain-level record of user activity.

### Activity Repository

Responsible for activity persistence operations.

* Records ```ActivityEvent``` instances
* Checks whether activity exists for a guild, user, and date
* Retrieves activity dates for a guild and user
* Abstracts storage operations from the rest of the application

The project contains both:

* ActivityRepository — in-memory implementation used for lightweight testing
* SQLiteActivityRepository — persistent implementation used by the application

### SQLite Activity Repository

Provides persistent activity storage using SQLite.

Activity is stored using:
```text
guild_id
user_id
activity_date
```

The database enforces one activity record per user, guild, and calendar date.

It supports:
* Stores activity by user ID and calendar date
* Enforces one activity record per user per date
* Supports activity existence checks
* Retrieves activity dates
* Persists data across application restarts
* Handles database connection lifecycle

Calendar dates are stored as ISO-8601 YYYY-MM-DD strings.

### Streak Service

Responsible for calculating streaks from activity dates.

* Calculates current streaks
* Calculates longest streaks
* Handles missing activity dates
* Handles empty activity history
* Contains no repository or Discord dependencies

### Activity Stats Service

Coordinates activity retrieval and streak calculations.

* Retrieves activity dates through the repository
* Calculates current streaks through StreakService
* Calculates longest streaks through StreakService
* Maintains guild and user context throughout the statistics flow

### Streak Command

Provides application-level behavior for the streak command.

* Receives guild ID, user ID, and current date
* Retrieves current and longest streaks through ActivityStatsService
* Formats the response
* Contains no Discord-specific logic

### Discord Streak Slash Command

Adapts the application-level streak command to Discord interactions.

* Receives a Discord interaction
* Extracts guild and user IDs
* Resolves the current local date
* Passes application-level values to StreakCommand
* Sends the resulting response through Discord

The command is exposed through Discord as:
```
/streak
```

### Membership Commands

The membership command layer allows users to manage their participation in the activity tracker directly through Discord.

The available commands are:

* /streak join — Join the activity tracker for the current guild.
* /streak leave — Leave the activity tracker for the current guild.
* /streak timezone — Select a new timezone for an existing membership.

Membership commands operate within the current Discord guild. A user’s membership in one guild does not determine their membership in another.

Timezone preferences are stored with membership data and are used when resolving the member’s local activity dates and current streak date.

Leaving the tracker removes the membership but preserves previously recorded activity history. Rejoining allows the user to resume participation without discarding that history.


### Configuration

Responsible for loading and validating application configuration.

Current configuration includes:

* Discord bot token

Environment variables are loaded from .env, while .env.example documents the required configuration without containing real credentials.

Tracker membership is not configured through environment variables. Membership is now managed at the application level and is scoped to individual Discord guilds.

### Application Entry Point

main.py acts as the composition root.

It:

* Creates application configuration
* Creates the application data directory
* Creates the SQLite activity repository
* Creates the membership repository
* Creates the activity qualification service
* Creates the activity date resolver
* Creates the streak service
* Creates the activity statistics service
* Creates the streak command
* Creates the event listener
* Creates the Discord gateway
* Injects dependencies between components
* Starts the Discord gateway
* Closes the SQLite repository when the application stops

Keeping dependency wiring in the composition root prevents construction logic from leaking into application components.



## Project Progress

### Phase 1 — Discord Gateway & Event Listener

#### Project Setup

* ✅ Create project repository
* ✅ Set up Python virtual environment
* ✅ Install discord.py
* ✅ Create .env file
* ✅ Configure .gitignore
* ✅ Verify project runs locally
* ✅ Configure test environment with pytest
* ✅ Add asynchronous testing support with pytest-asyncio

#### Discord Gateway

* ✅ Create DiscordGateway class
* ✅ Configure Discord intents
* ✅ Load bot token from configuration
* ✅ Start the Discord client
* ✅ Register on_message handler
* ✅ Register on_ready handler
* ✅ Translate Discord messages into MessageEvent
* ✅ Forward events to the application layer
* ✅ Keep Discord-specific logic isolated to the Gateway

#### Event Listener

* ✅ Create EventListener
* ✅ Receive application-level MessageEvent objects
* ✅ Check guild membership
* ✅ Filter messages by tracked user
* ✅ Ignore non-members
* ✅ Delegate activity qualification
* ✅ Resolve activity date
* ✅ Check whether activity already exists for the event date
* ✅ Convert qualifying messages into ActivityEvent objects
* ✅ Record the first qualifying activity of the day

#### Activity Qualification

* ✅ Create ActivityQualificationService
* ✅ Integrate qualification service with Event Listener
* ✅ Add tests for activity qualification
* ✅ Add tests for non-qualifying activity behavior
* ✅ Keep qualification logic isolated from event handling and persistence

#### Activity Domain Model

* ✅ Create ActivityEvent
* ✅ Add guild context to activity events
* ✅ Represent activity using guild, user, and calendar date
* ✅ Separate domain activity from Discord message details
* ✅ Add ActivityEvent tests

#### Activity Repository

* ✅ Create in-memory ActivityRepository
* ✅ Record ActivityEvent instances
* ✅ Query activity for a given date
* ✅ Retrieve activity dates for a user
* ✅ Use in-memory storage for lightweight tests
* ✅ Add SQLite persistence
* ✅ Enforce one activity per guild, user, and calendar date
* ✅ Test persistence across repository instances
* ✅ Test database lifecycle and cleanup

Timezone-Aware Activity Dates

* ✅ Create ActivityDateResolver
* ✅ Resolve timestamps using IANA timezones
* ✅ Load the default timezone from configuration
* ✅ Integrate date resolution into Event Listener
* ✅ Test timezone-specific date boundaries

#### Application Wiring

* ✅ Create application composition root
* ✅ Inject ActivityRepository into Event Listener
* ✅ Inject MembershipRepository into Event Listener
* ✅ Inject ActivityQualificationService into Event Listener
* ✅ Inject Activity Date Resolver
* ✅ Inject Event Listener into Discord Gateway
* ✅ Start the Gateway from the application entry point
* ✅ Close the SQLite repository when the application stops
* ✅ Test application dependency wiring

### Phase 2 — Activity History & Statistics

#### Activity History

* ✅ Add repository support for retrieving activity dates
* ✅ Return activity dates for a specific user
* ✅ Test activity date retrieval
* ✅ Add date-range activity queries
* ✅ Scope history queries by guild and user
* ✅ Test date-range query behavior

#### Streak Engine

* ✅ Create StreakService
* ✅ Calculate current streak
* ✅ Calculate longest streak
* ✅ Handle missing activity dates
* ✅ Handle empty activity history
* ✅ Test streak calculation behavior

#### Activity Statistics

* ✅ Create ActivityStatsService
* ✅ Coordinate activity history retrieval
* ✅ Coordinate current streak calculation
* ✅ Coordinate longest streak calculation
* ✅ Scope statistics by guild and user
* ✅ Test statistics service coordination

### Phase 3 — Discord Commands

#### Streak Command

* ✅ Create StreakCommand
* ✅ Keep command behavior independent of Discord
* ✅ Create DiscordStreakSlashCommand adapter
* ✅ Create CurrentDateResolver
* ✅ Register /streak application command
* ✅ Synchronize application commands with Discord
* ✅ Test command registration and invocation
* ✅ Verify /streak against live Discord activity

#### Live Activity Tracking

* ✅ Install/invite the Discord bot to a server
* ✅ Configure required Message Content intent
* ✅ Verify Discord Gateway connection
* ✅ Verify Discord message events are received
* ✅ Verify activity is persisted from live Discord messages
* ✅ Verify /streak reads persisted activity

### Phase 4 — Guild-Scoped Tracking

#### Guild Context

* ✅ Add guild context to MessageEvent
* ✅ Add guild context to ActivityEvent
* ✅ Propagate guild context through the message flow
* ✅ Scope activity persistence by guild
* ✅ Scope streak statistics by guild
* ✅ Test cross-guild activity isolation

#### Multiple Users

* ✅ Support multiple users within a guild
* ✅ Remove single-user filtering from Event Listener
* ✅ Add guild membership repository
* ✅ Scope membership by guild and user
* ✅ Test membership isolation
* ✅ Replace global tracked-user filtering with membership checks
* ✅ Remove obsolete tracked-user configuration

### Phase 5 — Membership Management

#### Persistent Membership

* ✅ Add SQLite-backed membership storage
* ✅ Persist guild and user membership
* ✅ Persist member timezone preferences
* ✅ Support membership lookup and removal
* ✅ Test membership persistence

#### Membership Commands

* ✅ Add /streak join
* ✅ Add /streak leave
* ✅ Add /streak timezone
* ✅ Prevent duplicate membership
* ✅ Handle leaving an inactive membership
* ✅ Test membership command behavior
* ✅ Preserve activity history when membership is removed
* ✅ Verify commands against a live Discord server

#### Timezone Management

* ✅ Provide a curated timezone selection
* ✅ Validate timezone selections
* ✅ Update existing member timezone preferences
* ✅ Persist timezone changes across application restarts

### Phase 6 — Activity Logging

* ✅ Create or locate a #daily-streak channel per guild
* ✅ Automatically create the channel if it does not exist
* ✅ Announce newly recorded daily activity
* ✅ Include the user’s current streak in activity notifications
* ✅ Keep Discord channel operations isolated in DiscordActivityNotifier
* ✅ Use a Discord user mention, falling back to the user ID when the member is not cached
* ✅ Notify only when new daily activity is recorded
* ✅ Calculate the updated streak using the recorded activity date
* ✅ Test notification delivery, channel creation, gateway integration, and application dependency wiring

### Phase 7 — Activity History & Statistics

#### Activity History

* ✅ Add date-range activity queries
* ✅ Implement /history
* ✅ Support a default seven-day history period
* ✅ Allow history periods between 1 and 30 days
* ✅ Display active and inactive days within the selected period
* ✅ Calculate the activity rate for the selected period
* ✅ Validate history command arguments
* ✅ Require tracker membership to access personal history
* ✅ Test history command behavior

#### Streak Statistics

* ✅ Display current and longest streaks through /streak
* ✅ Display recent activity count and activity rate
* ✅ Preserve the current streak through a one-day grace period
* ✅ Return a zero current streak when the grace period has elapsed
* ✅ Test streak calculations and recent activity statistics

### Phase 8 — Daily Streak Reminders

Planned work:

* ⬜ Allow members to opt in to daily streak reminders
* ⬜ Allow members to opt out of reminders
* ⬜ Configure a designated reminder channel for each guild
* ⬜ Schedule reminders according to each member’s configured timezone
* ⬜ Remind eligible members who have an active streak but have not recorded activity that day
* ⬜ Include the member’s current streak in reminder messages
* ⬜ Prevent duplicate reminders within the same local calendar day
* ⬜ Handle bot downtime and missed reminder times
* ⬜ Persist reminder preferences and delivery history across restarts
* ⬜ Test reminder eligibility, scheduling, persistence, and delivery

### Future Expansion

Potential future functionality includes:

* Multiple habits
* Configurable activity qualification rules
* Statistics and activity heatmaps
* Achievements
* Web dashboard

Additional functionality will be introduced as requirements emerge rather than adding abstractions prematurely.


## Before starting the bot, configure the required environment variables in .env:

DISCORD_TOKEN=your_bot_token

The configured timezone is used as the default timezone for the application. Individual members can subsequently select their own timezone through /streak timezone.

The Discord bot must have the required message-related intents enabled in the Discord Developer Portal. It must also be installed in the target Discord server with the appropriate permissions and application-command scope.

Once running, the bot receives Discord messages and records qualifying activity for users who have joined the tracker in the relevant guild.

Available commands:
```
/streak
/streak join
/streak leave
/streak timezone
```

The /streak command displays current and longest streak statistics. Membership commands manage participation in the tracker, while the timezone command allows existing members to update their local timezone preference.

Activity history and membership data are persisted in SQLite and survive application restarts.

## Development Philosophy

The project is being developed incrementally with an emphasis on learning, maintainability, and clear architectural boundaries.

Key principles include:

* Separation of concerns
* Dependency injection
* Test-driven development
* Asynchronous programming
* Clear application boundaries
* Discord-specific logic isolated from application logic
* Persistence isolated behind repository implementations
* Guild context propagated explicitly through application flows
* Small, focused Git commits
* Incremental architectural changes
* Avoiding unnecessary abstractions until requirements justify them

The project favors simple designs that can evolve as requirements become clearer.

## Testing

The project uses pytest and pytest-asyncio for automated testing.

Current test suite: 140 tests passing ✅

Testing covers:

* Configuration loading and validation
* Discord Gateway initialization, startup, and event-handler registration
* Discord message translation and application-level event processing
* Guild membership filtering and multi-user activity processing
* Activity qualification and first-activity-of-the-day detection
* MessageEvent and ActivityEvent behavior
* In-memory activity and membership repositories
* SQLite activity and membership repositories
* Guild-scoped persistence and persistence across repository instances
* Activity-date retrieval and date-range queries
* Timezone-aware activity-date and current-date resolution
* Application dependency wiring and message-flow integration
* Current and longest streak calculations, including the one-day grace period
* Recent activity statistics and activity-rate calculations
* Streak command behavior and Discord command invocation
* Discord application-command registration
* Membership service validation, lifecycle, and persistence
* Timezone selection and update behavior
* Activity history command behavior, including date-range validation and membership requirements
* Activity notification delivery and automatic channel creation
* Notification suppression when no new daily activity is recorded
* Fallback mentions for uncached Discord members

Tests are organized into unit and integration tests. The suite is expanded alongside new functionality to verify new behavior and guard against regressions.

```text
tests/
├── integration/
│   ├── test_main.py
│   └── test_message_flow.py
└── unit/
    ├── adapters/
    │   ├── test_discord_activity_notifier.py
    │   └── test_discord_gateway.py
    ├── commands/
    │   ├── test_discord_history_slash_command.py
    │   ├── test_discord_streak_join_slash_command.py
    │   ├── test_discord_streak_leave_slash_command.py
    │   ├── test_discord_streak_slash_command.py
    │   ├── test_discord_streak_timezone_slash_command.py
    │   ├── test_discord_timezone_select.py
    │   ├── test_history_command.py
    │   ├── test_streak_command.py
    │   ├── test_timezone_select_view.py
    │   └── test_timezone_update_select.py
    ├── models/
    │   ├── test_activity_event.py
    │   ├── test_message_event.py
    │   └── test_tracker_member.py
    ├── repositories/
    │   ├── test_activity_repository.py
    │   ├── test_membership_repository.py
    │   ├── test_sqlite_activity_repository.py
    │   └── test_sqlite_membership_repository.py
    ├── services/
    │   ├── test_activity_date_resolver.py
    │   ├── test_activity_qualification.py
    │   ├── test_activity_stats_service.py
    │   ├── test_current_date_resolver.py
    │   ├── test_membership_service.py
    │   └── test_streak_service.py
    ├── test_config.py
    ├── test_event_listener.py
    └── test_timezones.py
```

The test suite is expanded alongside new functionality to ensure existing behavior remains intact.

## Project Structure

```
discord-habit-tracker/
├── src/
│   └── discord_habit_tracker/
│       ├── adapters/
│       │   └── discord_activity_notifier.py
│       ├── commands/
│       │   ├── discord_history_slash_command.py
│       │   ├── discord_streak_join_slash_command.py
│       │   ├── discord_streak_leave_slash_command.py
│       │   ├── discord_streak_slash_command.py
│       │   ├── discord_streak_timezone_slash_command.py
│       │   ├── discord_timezone_select.py
│       │   ├── discord_timezone_update_select.py
│       │   ├── history_command.py
│       │   ├── streak_command.py
│       │   ├── timezone_select_view.py
│       │   └── timezone_update_select_view.py
│       ├── data/
│       │   └── activity_tracker.db
│       ├── models/
│       │   ├── activity_event.py
│       │   ├── message_event.py
│       │   └── tracker_member.py
│       ├── repositories/
│       │   ├── activity_repository.py
│       │   ├── membership_repository.py
│       │   ├── sqlite_activity_repository.py
│       │   └── sqlite_membership_repository.py
│       ├── services/
│       │   ├── activity_date_resolver.py
│       │   ├── activity_qualification_service.py
│       │   ├── activity_stats_service.py
│       │   ├── current_date_resolver.py
│       │   ├── exceptions.py
│       │   ├── membership_service.py
│       │   └── streak_service.py
│       ├── __init__.py
│       ├── config.py
│       ├── discord_gateway.py
│       ├── event_listener.py
│       ├── main.py
│       └── timezones.py
├── tests/
│   ├── integration/
│   │   ├── test_main.py
│   │   └── test_message_flow.py
│   └── unit/
│       ├── adapters/
│       ├── commands/
│       ├── models/
│       ├── repositories/
│       ├── services/
│       ├── test_config.py
│       ├── test_event_listener.py
│       └── test_timezones.py
├── pyproject.toml
├── readme.md
└── requirements.txt
```

The project structure will evolve as additional components are introduced.

