# Personal Discord Habit & Activity Tracker

A production-quality Discord bot that automatically tracks daily activity and habit streaks.

> **Current Status:** ✅ Phase 7 — Activity History & Statistics Complete · ✅ Phase 8 — Daily Streak Reminders Implementation & Automated Testing Complete · ⏳ Live Discord Verification Pending

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
├── ✅ Persistent reminder opt-in preference
├── ✅ Default reminder time (9 PM member-local time)
├── ✅ Timezone-aware daily scheduling
├── ✅ Remind eligible users with an active streak
├── ✅ Prevent duplicate reminders per local calendar day
├── ✅ Skip missed reminders after bot downtime
├── ✅ Persist reminder delivery history
├── ✅ Scheduler lifecycle and failure handling
├── ✅ Automated scheduling, persistence, and delivery tests
└── ⬜ Live Discord verification

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

Members can also opt in to daily streak reminders. The reminder scheduler checks each participating member according to their configured timezone and sends a reminder at the default time of 9 PM local time, provided they have an active streak and have not recorded activity for that local calendar day.

Reminders are delivered through the guild's `#daily-streak` channel. Delivery history is persisted to prevent duplicate reminders for the same member, guild, and local calendar date. Missed reminders are skipped rather than sent retrospectively when the bot restarts.

The project is developed incrementally, with an emphasis on clean architecture, testability, dependency injection, and small, focused changes.


## Architecture

The project is structured around separating Discord-specific communication from application logic and persistence.

```text
                         main.py
                    (Composition Root)
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
       DiscordGateway  EventListener  DailyReminderScheduler
             │             │              │
             │             │              ├── ReminderEligibilityService
             │             │              │
             │             │              ├── ActivityStatsService
             │             │              │
             │             │              └── DiscordActivityNotifier
             │             │
             │             ├── MembershipRepository
             │             ├── ActivityQualificationService
             │             ├── ActivityDateResolver
             │             └── ActivityRepository
             │
             ├── Discord Slash Command Adapters
             │       │
             │       ├── StreakCommand
             │       ├── HistoryCommand
             │       └── MembershipService
             │
             └── DiscordActivityNotifier

                           │
                           ▼
                    SQLite Repositories
                           │
                           ▼
                     SQLite Storage
```

The application follows a layered architecture that separates Discord-specific communication, application orchestration, business logic, and data persistence. The main.py module acts as the composition root, responsible for initializing the application's dependencies and connecting the various components.

The DiscordGateway translates incoming Discord messages into application-level MessageEvent objects and forwards them to the EventListener. The listener coordinates membership validation, activity qualification, timezone-aware date resolution, and activity recording through the relevant repositories and services.

Application commands handle streak and activity history operations independently of Discord. Discord-specific slash-command adapters handle interaction responses and delegate application logic to these commands and services. Membership operations are managed through MembershipService, which validates membership changes and timezone settings before updating the repository.

Data persistence is handled through repository abstractions, with SQLite implementations providing storage for activity records, tracker memberships, and reminder delivery history. The statistics layer delegates streak calculations to StreakService, while the daily reminder scheduler coordinates scheduled notifications through ReminderEligibilityService, ActivityStatsService, and DiscordActivityNotifier.

This separation keeps Discord integration, application orchestration, business logic, and persistence independently testable, while allowing infrastructure implementations to be replaced without rewriting the core application logic.


```
DailyReminderScheduler
        |
        ├── MembershipRepository
        |       |
        |       └── Retrieve reminder-enabled members
        |
        ├── ReminderEligibilityService
        |       |
        |       ├── Check reminder preference
        |       ├── Check today's activity
        |       ├── Check current streak
        |       └── Check previous delivery
        |
        ├── ActivityStatsService
        |       |
        |       └── Retrieve current streak
        |
        ├── DiscordActivityNotifier
        |       |
        |       └── Send reminder to #daily-streak
        |
        └── ReminderDeliveryRepository
                |
                └── SQLite Storage
```
The DailyReminderScheduler operates independently of the incoming-message activity pipeline. It periodically checks reminder-enabled members and determines whether their local reminder time has arrived.

ReminderEligibilityService evaluates whether a member should receive a reminder by checking their reminder preference, current-day activity, current streak, and previous delivery history.

When a reminder is eligible, the scheduler delegates notification delivery to DiscordActivityNotifier. Successful deliveries are recorded through the ReminderDeliveryRepository to prevent duplicate reminders for the same guild, member, and local calendar date.


## Streak Flow

```
Discord /streak stats
        │
        ▼
DiscordStreakSlashCommand
        │
        ├── MembershipRepository
        │       └── Retrieve tracker member
        │
        ├── CurrentDateResolver
        │       └── Resolve date using member timezone
        │
        ▼
StreakCommand
        │
        ▼
ActivityStatsService
        │
        ├── ActivityRepository
        │       └── Retrieve activity dates
        │
        ├── StreakService
        │       ├── Calculate current streak
        │       └── Calculate longest streak
        │
        └── ActivityRepository
                └── Retrieve last 30 days
                        │
                        ▼
                 Recent activity statistics
                        │
                        ▼
                Formatted response
                        │
                        ▼
                Discord interaction
```

The /streak stats command is handled by DiscordStreakSlashCommand, which verifies tracker membership and resolves the current date using the member's configured timezone. It then delegates the request to StreakCommand, which coordinates the retrieval and formatting of activity statistics.

ActivityStatsService retrieves the user's recorded activity dates through ActivityRepository and delegates current and longest streak calculations to StreakService. It also calculates recent activity statistics over the last 30 calendar days, including active days and activity rate.

StreakService contains the streak calculation logic independently of Discord and database implementations. The current streak counts consecutive activity days ending today, or yesterday if no activity has been recorded today. The longest streak identifies the longest uninterrupted sequence of recorded activity dates.


## Activity Notification Flow

When a message results in a newly recorded ActivityEvent, the Discord gateway retrieves the user’s updated streak through ActivityStatsService and delegates the announcement to DiscordActivityNotifier.

```
Immediate Activity Notification
────────────────────────────────

Discord Message
      │
      ▼
DiscordGateway
      │
      ▼
EventListener
      │
      ▼
New ActivityEvent?
      │
      ▼
ActivityStatsService
      │
      ▼
DiscordActivityNotifier.notify()
      │
      │
      └──────────────────┐
                         │
                         ▼
                  #daily-streak
                         ▲
                         │
      ┌──────────────────┘
      │
DiscordActivityNotifier.notify_reminder()
      ▲
      │
DailyReminderScheduler
      │
      ▼
ReminderEligibilityService
      │
      ▼
Eligible Member?
```

When a Discord message results in a newly recorded `ActivityEvent`, the
Discord gateway retrieves the user's updated streak through
`ActivityStatsService` and delegates the announcement to
`DiscordActivityNotifier.notify()`.

Notifications are sent only when the event listener reports newly recorded
activity. Messages that do not produce a new activity record do not trigger
activity notifications.

Daily reminders follow a separate scheduled flow. `DailyReminderScheduler`
checks members with reminders enabled and uses `ReminderEligibilityService`
to determine whether they should receive a reminder. Eligible members
receive a notification through `DiscordActivityNotifier.notify_reminder()`.

`DiscordActivityNotifier` handles both notification formats and the shared
channel lookup. It reuses the guild's `#daily-streak` channel when available,
or creates it when missing. It also resolves the member's mention, falling
back to a raw Discord mention if the member is not cached.

The gateway and scheduler coordinate their respective flows without
implementing notification formatting themselves.


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


### Database Scoping

Guild isolation is enforced through composite primary keys in SQLite:

| Table | Composite Primary Key | Purpose |
|---|---|---|
| `members` | `(guild_id, user_id)` | Maintains independent membership, timezone, and reminder preferences per guild |
| `activities` | `(guild_id, user_id, activity_date)` | Allows one activity record per user per guild per calendar date |
| `reminder_deliveries` | `(guild_id, user_id, reminder_date)` | Tracks reminder deliveries independently for each guild and date |

Repository queries also include `guild_id` when retrieving, updating, or deleting guild-specific records.

This ensures that activity history, streak calculations, membership settings, and reminder delivery tracking remain isolated between Discord servers.


## Components

### Discord Gateway

Responsible for communicating with Discord and translating Discord events into application-level events.

- Connects to Discord
- Configures required Discord intents
- Receives Discord messages
- Converts Discord messages into MessageEvent
- Forwards events to the EventListener
- Registers Discord application commands
- Synchronizes application commands with Discord
- Starts and manages the daily reminder scheduler
- Coordinates post-activity notifications through DiscordActivityNotifier
- Contains no activity qualification or streak calculation business logic

The gateway acts as the integration layer between Discord and the application. It handles Discord-specific interactions while delegating application behaviour to the appropriate services and components.

Registered commands include:

- `/streak stats`
- `/streak join`
- `/streak leave`
- `/streak timezone`
- `/history`

### Discord Activity Notifier

Responsible for sending activity announcements and daily reminders to Discord guilds.

It supports two notification types:

- Activity notifications — Announces when a member completes their activity for the day and displays their current streak.
- Reminder notifications — Reminds eligible members to record their activity before the day ends.

Both notification types:

- Use the guild's `#daily-streak` channel
- Reuse the channel if it already exists
- Create the channel if it does not exist
- Resolve the member's Discord mention

The notifier handles Discord message formatting and delivery, keeping notification presentation separate from the gateway and reminder scheduling logic.

### Daily Reminder Scheduler

Responsible for periodically checking whether tracker members should receive daily activity reminders.

- Runs as a background task managed by DiscordGateway
- Retrieves members who have enabled daily reminders
- Resolves each member's local date and time using their configured timezone
- Checks whether the reminder time and delivery window have been reached
- Checks whether the scheduler started after the scheduled reminder time
- Delegates reminder eligibility checks to ReminderEligibilityService
- Retrieves the member's current streak
- Sends reminders through DiscordActivityNotifier
- Records successful reminder deliveries through ReminderDeliveryRepository

The scheduler handles timing and delivery coordination without implementing reminder eligibility rules or Discord notification formatting itself.

### Reminder Eligibility Service

Determines whether a tracker member is eligible to receive a daily activity reminder.

It checks that:

- The member exists in the current guild
- Daily reminders are enabled
- The member has not recorded activity for the current local date
- The member has an active streak to maintain
- A reminder has not already been delivered for that guild, user, and date

The service keeps reminder eligibility rules separate from the scheduler's timing and delivery responsibilities.

### Event Listener

Responsible for orchestrating application-level message processing.

- Receives MessageEvent
- Retrieves tracker membership using guild ID and user ID
- Delegates activity qualification to ActivityQualificationService
- Resolves the message timestamp to the member's configured local calendar date
- Checks whether activity has already been recorded for that guild, user, and date
- Creates an ActivityEvent for qualifying, previously unrecorded activity
- Records the activity through ActivityRepository

The Event Listener coordinates application-level processing without handling Discord-specific communication or implementing activity qualification rules itself.

Membership and activity persistence are provided through their respective repositories.

### Membership Repository

Responsible for persisting tracker membership and member preferences.

Membership is scoped to a Discord guild and user:

(guild_id, user_id)

The project provides both:

- MembershipRepository — in-memory implementation used for lightweight testing
- SQLiteMembershipRepository — persistent implementation used by the application

It supports:

- Adding a user to a guild's tracker
- Retrieving a user's membership
- Removing a user from a guild's tracker
- Updating a member's configured timezone
- Updating reminder preferences
- Retrieving members who have enabled daily reminders
- Isolating membership and preferences between guilds
- Persisting membership data across application restarts

Membership operations are coordinated by MembershipService, which validates timezone selections and manages membership-related business rules.

Discord slash-command adapters expose these operations through `/streak join`, `/streak leave`, and `/streak timezone`.

### Reminder Delivery Repository

Responsible for tracking successfully delivered daily reminders.

The project provides:

- ReminderDeliveryRepository — in-memory implementation used for lightweight testing
- SQLiteReminderDeliveryRepository — persistent implementation used by the application

Reminder deliveries are scoped by:

```text
guild_id
user_id
reminder_date
```

The repository supports:
- Recording successful reminder deliveries
- Checking whether a reminder has already been delivered
- Preventing duplicate delivery records
- Persisting delivery history across application restarts
The SQLite implementation enforces uniqueness through a composite primary key:

```sql
PRIMARY KEY (guild_id, user_id, reminder_date)
```


### Activity Qualification Service

Responsible for determining whether an incoming message event qualifies as activity.

The current implementation uses a deliberately simple rule:

- Every message from a tracked member qualifies as activity.

The service is isolated from the Event Listener so that qualification rules can evolve independently of event processing and persistence.

### Activity Date Resolver

Responsible for converting message timestamps into local calendar dates.

- Uses the member's configured IANA timezone
- Uses Python's zoneinfo module
- Converts message timestamps into the member's local calendar date
- Keeps timezone handling separate from event processing

This ensures activity is recorded according to the member's configured local day rather than the Discord server or machine timezone.

### Current Date Resolver

Responsible for resolving the current calendar date in a member's configured timezone.

- Uses the member's configured IANA timezone
- Obtains the current timezone-aware timestamp through SystemClock
- Converts the timestamp into the member's local calendar date
- Keeps current-date resolution separate from Discord command handling

This allows commands such as `/streak stats` and `/history` to operate according to the member's local calendar date rather than the machine's local timezone.

### System Clock

Provides the current timezone-aware timestamp to application components.

- Supplies the current time through a central abstraction
- Keeps time retrieval separate from business logic
- Supports consistent time-dependent behaviour
- Allows time-dependent components to be tested independently of the system clock

The clock is injected into components that need to determine the current date or time.



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

ActivityEvent represents the application-level record created when a message qualifies as activity.

#### TrackerMember
Represents a user's membership in a guild's activity tracker:

```
guild_id
user_id
timezone
reminders_enabled
```


Separating ```MessageEvent``` from ```ActivityEvent``` prevents Discord-specific message details from leaking into the activity domain.

MessageEvent represents the incoming event from Discord, while ActivityEvent represents the application’s domain-level record of user activity.

### Activity Repository

Responsible for defining activity persistence operations.

- Records ActivityEvent instances
- Checks whether activity exists for a guild, user, and date
- Retrieves all activity dates for a guild and user
- Retrieves activity dates within an inclusive date range
- Abstracts activity storage operations from the rest of the application

The project provides both:

- ActivityRepository — in-memory implementation used for lightweight testing
- SQLiteActivityRepository — persistent implementation used by the application

This abstraction allows application services to work with activity data without depending directly on the underlying storage implementation.

### SQLite Activity Repository

Provides persistent activity storage using SQLite.

Activity is stored using:

```text
guild_id
user_id
activity_date
```

The database enforces the following composite primary key:

```
PRIMARY KEY (guild_id, user_id, activity_date)
```

It supports:
- Recording activity while ignoring duplicate records
- Enforcing one activity record per user, guild, and calendar date
- Checking whether activity exists for a specific date
- Retrieving all activity dates for a guild and user
- Retrieving activity dates within an inclusive date range
- Persisting activity across application restarts
- Managing the database connection lifecycle
Calendar dates are stored as ISO-8601 YYYY-MM-DD strings.

The repository also handles the legacy activity table schema. If an existing table does not contain guild_id, it is dropped and recreated using the guild-scoped schema.

### Streak Service

Responsible for calculating streaks from recorded activity dates.

- Calculates current streaks
- Calculates longest streaks
- Handles missing activity dates
- Handles empty activity history
- Contains no repository or Discord dependencies

The current streak calculation allows for a one-day grace period. If no activity has been recorded today, the calculation starts from yesterday instead. This prevents an incomplete current day from immediately breaking an existing streak.

### Activity Stats Service

Coordinates activity retrieval and streak calculations.

- Retrieves activity dates through ActivityRepository
- Calculates current streaks through StreakService
- Calculates longest streaks through StreakService
- Retrieves activity dates within a specified date range
- Calculates recent activity statistics over the last 30 calendar days
- Maintains guild and user context throughout the statistics flow

Recent activity statistics include:

- Total days tracked
- Number of active days
- Activity rate as a percentage

The service coordinates data retrieval and calculations without implementing Discord-specific behaviour.

### Streak Command

Provides application-level behaviour for retrieving and presenting a member's streak statistics.

- Receives guild ID, user ID, and current date
- Retrieves current and longest streaks through ActivityStatsService
- Retrieves recent activity statistics
- Formats the statistics into a response
- Contains no Discord-specific logic

The command operates independently of Discord interactions and can be tested without connecting to Discord.

### History Command

Provides application-level behaviour for retrieving and presenting a member's activity history.

- Receives guild ID, user ID, start date, and end date
- Validates the requested date range
- Retrieves activity dates through ActivityRepository
- Generates a daily activity calendar
- Calculates the activity rate for the requested period
- Formats the result without Discord-specific logic

The command provides a date-based overview of recorded activity for a member.

### Discord History Slash Command

Adapts the application-level history command to Discord interactions.

- Receives a Discord interaction
- Extracts guild and user IDs
- Checks tracker membership in the current guild
- Validates the requested history period
- Resolves the current local date using the member's configured timezone
- Calculates the requested date range
- Delegates history retrieval to HistoryCommand
- Sends the resulting activity calendar through Discord

The command is exposed through Discord as:

```text
/history
```

The command supports history periods between 1 and 30 days.


### Discord Streak Slash Command

Adapts the application-level streak command to Discord interactions.

- Receives a Discord interaction
- Extracts guild and user IDs
- Retrieves the user's tracker membership
- Resolves the current local date using the member's configured timezone
- Passes application-level values to StreakCommand
- Sends the resulting statistics response through Discord

The command is exposed through Discord as:

```text
/streak stats
```

If the user is not registered with the tracker in the current guild, the command prompts them to join.


### Membership Service

Coordinates tracker membership operations through MembershipRepository.

- Adds users to the tracker for a specific guild
- Removes users from tracker membership
- Updates member timezone preferences
- Updates daily reminder preferences
- Validates timezone selections using Python's zoneinfo
- Handles missing membership through application-level exceptions

Membership operations are scoped to the current guild and user.

The service keeps membership-related business rules separate from Discord interaction handling and database persistence.


### Membership Commands

The membership command layer allows users to manage their participation in the activity tracker directly through Discord.

The available commands are:

- `/streak join` — Join the activity tracker for the current guild.
- `/streak leave` — Leave the activity tracker for the current guild.
- `/streak timezone` — Update the timezone for an existing membership.

The Discord command adapters delegate membership operations to MembershipService.

Timezone selection is handled through Discord-specific selection views:

- TimezoneSelectView — Allows new members to select their timezone when joining.
- TimezoneUpdateSelectView — Allows existing members to update their timezone.

Membership commands operate within the current Discord guild. A user's membership in one guild does not determine their membership in another.

Timezone preferences are stored with membership data and are used when resolving local activity dates and current streak dates.

Leaving the tracker removes the membership but preserves previously recorded activity history. Rejoining allows the user to resume participation without discarding that history.


### Configuration

Responsible for loading and validating application configuration.

Current configuration includes:

- Discord bot token
- Tracked user IDs

Environment variables are loaded from `.env`, while `.env.example` documents the required configuration without containing real credentials.

Tracked user IDs determine which Discord users' messages are monitored by the application.

Tracker membership, timezone preferences, and reminder settings are managed at the application level and persisted through their respective repositories rather than configured through environment variables.

### Application Entry Point

`main.py` acts as the application's composition root.

It is responsible for constructing application dependencies, wiring components together, and managing the application lifecycle.

Its responsibilities include:

**Configuration and persistence**
- Loads application configuration
- Creates the application data directory
- Initializes the SQLite activity repository
- Initializes the SQLite membership repository
- Initializes the SQLite reminder delivery repository

**Service construction**
- Creates MembershipService
- Creates ActivityQualificationService
- Creates ActivityDateResolver
- Creates CurrentDateResolver
- Creates SystemClock
- Creates StreakService
- Creates ActivityStatsService
- Creates ReminderEligibilityService
- Creates DiscordActivityNotifier

**Application commands and event processing**
- Creates StreakCommand
- Creates HistoryCommand
- Creates EventListener
- Injects the event listener into DiscordGateway

**Discord and reminder integration**
- Creates DiscordGateway with the required commands, repositories, services, and notifier
- Creates DailyReminderScheduler
- Injects the scheduler into DiscordGateway

**Application lifecycle**
- Starts the Discord gateway
- Closes all SQLite repository connections when the application stops

All SQLite repositories share the same database file:

```text
data/
└── activity_tracker.db
```

Keeping dependency construction in the composition root prevents infrastructure setup and object creation from leaking into application components. It also makes dependencies explicit and supports independent testing of individual components.

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

Completed:

* ✅ Allow members to opt in to daily streak reminders
* ✅ Allow members to opt out of reminders
* ✅ Use a designated `#daily-streak` channel for activity announcements and reminders
* ✅ Schedule reminders according to each member's configured timezone
* ✅ Remind eligible members who have an active streak but have not recorded activity that day
* ✅ Include the member's current streak in reminder messages
* ✅ Prevent duplicate reminders within the same local calendar day
* ✅ Handle scheduler startup after a member's scheduled reminder time
* ✅ Persist reminder preferences and delivery history across restarts
* ✅ Test reminder eligibility, scheduling, persistence, and delivery

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

Current test suite: 185 tests passing ✅

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
* Reminder eligibility checks, including membership, reminder preferences, activity status, and active streak requirements
* Daily reminder scheduling and timezone-aware reminder windows
* Reminder suppression for duplicate deliveries and missed scheduled times
* Reminder delivery through Discord and notification formatting
* In-memory and SQLite reminder delivery repositories
* Reminder preference and delivery-history persistence across restarts
* Reminder scheduler lifecycle and application integration

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
    │   ├── test_sqlite_membership_repository.py
    │   └── test_sqlite_reminder_delivery_repository.py
    ├── services/
    │   ├── test_activity_date_resolver.py
    │   ├── test_activity_qualification.py
    │   ├── test_activity_stats_service.py
    │   ├── test_current_date_resolver.py
    │   ├── test_daily_reminder_scheduler.py
    │   ├── test_membership_service.py
    │   ├── test_reminder_eligibility_service.py
    │   └── test_streak_service.py
    ├── test_config.py
    ├── test_event_listener.py
    └── test_timezones.py
```

The test suite is expanded alongside new functionality to ensure existing behavior remains intact.

## Project Structure

```
discord-habit-tracker/
├── data/
│   └── activity_tracker.db
├── src/
│   └── discord_habit_tracker/
│       ├── adapters/
│       │   └── discord_activity_notifier.py
│       ├── commands/
│       │   ├── __init__.py
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
│       ├── models/
│       │   ├── __init__.py
│       │   ├── activity_event.py
│       │   ├── message_event.py
│       │   └── tracker_member.py
│       ├── repositories/
│       │   ├── activity_repository.py
│       │   ├── membership_repository.py
│       │   ├── sqlite_activity_repository.py
│       │   ├── sqlite_membership_repository.py
│       │   └── sqlite_reminder_delivery_repository.py
│       ├── services/
│       │   ├── activity_date_resolver.py
│       │   ├── activity_qualification_service.py
│       │   ├── activity_stats_service.py
│       │   ├── current_date_resolver.py
│       │   ├── daily_reminder_scheduler.py
│       │   ├── exceptions.py
│       │   ├── membership_service.py
│       │   ├── reminder_eligibility_service.py
│       │   ├── streak_service.py
│       │   └── system_clock.py
│       ├── __init__.py
│       ├── config.py
│       ├── discord_gateway.py
│       ├── event_listener.py
│       ├── main.py
│       └── timezones.py
├── tests/
|   ...
├── .env.example
├── .gitattributes
├── .gitignore
├── pyproject.toml
├── readme.md
└── requirements.txt
```

The project structure will evolve as additional components are introduced.

