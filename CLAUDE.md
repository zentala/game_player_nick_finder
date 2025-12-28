# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Environment Setup
```bash
# Activate virtual environment
pipenv shell

# Install dependencies
pipenv install

# Apply database migrations
python manage.py migrate

# Load test fixtures (REQUIRED before E2E tests)
pnpm load:fixtures
# Or platform-specific:
# Windows: .\load_fixtures.ps1
# Unix/Linux/MacOS: ./load_fixtures.sh
```

### Development Server
```bash
# Run Django development server
python manage.py runserver

# Server will be available at http://localhost:8000
```

### Database Management
```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (interactive)
python manage.py createsuperuser
# Or use automated scripts:
# Windows: .\create_superuser.ps1
# Unix: ./create_superuser.sh

# Django shell for debugging
python manage.py shell

# Reset database (development only)
rm db.sqlite3
rm app/migrations/000*.py
python manage.py makemigrations
python manage.py migrate
pnpm load:fixtures
```

### Testing
```bash
# Run all Playwright E2E tests
pnpm test:e2e

# Run specific test file
pnpm test:e2e tests/e2e/feature-name.spec.ts

# Run tests in UI mode (interactive)
pnpm test:e2e:ui

# Run tests in headed mode (see browser)
pnpm test:e2e:headed

# Debug tests
pnpm test:e2e:debug

# CRITICAL: Load fixtures before running E2E tests
pnpm load:fixtures
```

### Test Users (from fixtures)
- `testuser` / `testpass123` - Main test user with multiple characters
- `otheruser` / `pass` - Secondary test user for interactions
- `privateuser` / `testpass123` - User with private profile

## High-Level Architecture

### Core Concept: Character-Centric System
**CRITICAL**: This is NOT a typical user-to-user social platform. Instead, it's **character-centric**:
- Users create multiple gaming **Characters** (different nicknames from different games)
- All social interactions (friendships, messaging, blocking) happen **between Characters**, not Users
- Example: User "John" can have characters "Dragonslayer99" (WoW) and "ProSniper" (CS:GO) with separate friend lists

### Key Architectural Patterns

#### 1. POKE System - Messaging Gateway
**CRITICAL**: Users cannot send direct messages. The flow is:
1. User A's character sends a **POKE** (100 char max, no URLs/emails) to User B's character
2. User B can: Respond, Ignore, or Block
3. **Only after mutual POKE exchange**, full messaging is unlocked
4. This prevents spam and maintains privacy

See: `docs/architecture/poke-system-architecture.md`

#### 2. Character-Based Relationships
All social features are character-to-character:
- **CharacterFriend**: Bidirectional friendships between characters (not users)
- **CharacterFriendRequest**: Pending/accepted/declined friend requests
- **Message**: Character A sends to Character B (with privacy modes)
- **CharacterBlock**: Character A blocks Character B (prevents POKEs, messages, friend requests)

Example: User "Alice" can have character "MageQueen" friends with character "WarriorKing", while her other character "SneakyRogue" is NOT friends with "WarriorKing".

#### 3. Privacy & Identity System
Messages support two privacy modes:
- **ANONYMOUS**: Sender's character nickname visible, but not user identity
- **REVEAL_IDENTITY**: Full user profile visible (controlled via CharacterIdentityReveal model)
- Identity reveals can be granted or revoked at any time

#### 4. URL Routing Pattern
- Character detail: `/character/<nickname>-<hash_id>/` (hash_id is auto-generated 10-char unique ID)
- Messages: `/messages/?character=<id>&thread_id=<uuid>` (thread_id groups conversation)
- POKEs: `/pokes/`, `/pokes/send/`, `/pokes/<uuid>/`
- Blocking: `/characters/block/`, `/characters/blocked/`

### Database Model Relationships

```
User (CustomUser with UUID pk)
├─> Character (1:N) - User can have multiple gaming personas
│   ├─> Game (N:1) - Each character belongs to one game
│   ├─> CharacterProfile (1:1) - Custom bio, screenshots, memories
│   ├─> CharacterFriend (N:N via through model) - Character-to-character friendships
│   ├─> CharacterFriendRequest (N:N as sender/receiver)
│   ├─> Message (N:N as sender/receiver) - Character-to-character messaging
│   ├─> Poke (N:N as sender/receiver) - Initial contact mechanism
│   ├─> CharacterBlock (N:N as blocker/blocked) - General blocking
│   ├─> PokeBlock (N:N) - Legacy POKE-specific blocking
│   └─> CharacterIdentityReveal (N:N as revealer/revealed_to)
└─> User Profile Fields: birthday, gender, profile_visibility, social links

Game
├─> GameCategory - Hierarchical organization
├─> Character (1:N)
└─> Vote - Game proposal voting system
```

### View Architecture

**Class-Based Views (CBVs)** with mixins:
- `BaseViewMixin`: Adds `current_page` to context for navigation highlighting
- `LoginRequiredMixin`: Restricts to authenticated users

**Common Pattern**:
```python
class FeatureView(LoginRequiredMixin, BaseViewMixin, ListView):
    model = ModelName
    template_name = 'app/feature.html'
    context_object_name = 'objects'
    current_page = 'feature'  # For navbar highlighting
```

**API Views** use Django REST Framework ViewSets with custom actions.

### Template Organization

Templates use inheritance pattern:
```
base.html (root)
  └─> base_navbar.html (navigation)
  └─> base_head.html (meta, CSS)
  └─> base_notifications.html (Django messages)
  └─> base_footer.html
  └─> base_scripts.html (JS)
    └─> containers/default.html (wrapper)
      └─> Feature-specific templates
```

**Content/partial pattern**: Many views have `_content.html` variants for HTMX/AJAX updates without full page reload.

### Utility Functions (app/utils.py)

Critical helper functions:
- `is_blocked(blocker_character, blocked_character)`: Check if blocking exists
- `can_send_poke(sender_character, receiver_character)`: Validates POKE rules (rate limit, blocking, cooldown)
- `can_send_message(sender_character, receiver_character)`: Checks if POKE unlock exists
- `validate_poke_content(content)`: Content filtering (no URLs, emails, profanity)
- `get_gravatar_url(email)`: Generate avatar from email

### Critical Business Rules

1. **POKE Rate Limiting**: Max 5 POKEs per user per 24 hours (`settings.POKE_MAX_PER_USER_PER_DAY`)
2. **POKE Cooldown**: 30 days between POKEs to same character (`settings.POKE_COOLDOWN_DAYS`)
3. **Blocking Precedence**: `CharacterBlock` takes priority over `PokeBlock`
4. **Unique Character Identifier**: `hash_id` (10 chars) auto-generated on save, used in URLs
5. **Character Uniqueness**: (user, nickname, game) combination must be unique

### Session & Superuser Management

**Fixture Loading Workflow**:
1. First time: Run `create_superuser.ps1` (Windows) or `create_superuser.sh` (Unix)
2. Credentials saved to `.dot/sudo_user` (in .gitignore, never committed)
3. All seeding scripts (`load_fixtures.*`) automatically create superuser after loading data
4. Idempotent: Safe to run multiple times (skips if user exists)

**Session Tracking**:
- Sessions recorded in `.cursor/sessions/YYYY-MM-DD_HH-MM.md`
- Created at conversation start (not immediately - add title when scope is clear)
- Updated after completing work or major milestones

## Testing Requirements

### Mandatory TDD Workflow
**CRITICAL**: Every feature MUST follow Test-Driven Development:
1. **Red Phase**: Write Playwright test first (failing test)
2. **Green Phase**: Implement feature to pass test
3. **Refactor Phase**: Clean up code while keeping tests green
4. **NEVER** commit code without corresponding E2E tests

### Test Coverage Requirements
- Minimum 80% E2E test coverage for all user flows
- All critical paths must have Playwright tests
- Tests must use seeded fixtures (`pnpm load:fixtures`)

### Test Structure
```
tests/e2e/
├── characters/         # Character CRUD, profiles
├── friends/            # Friend requests, friend lists
├── messaging/          # Conversations, message sending
├── blocking/           # Block/unblock, blocked list
├── pokes/             # POKE system tests
├── profile/            # User profile display/edit
└── navigation/         # Navigation menu tests
```

## Special Configurations

### Development Settings (settings/local.py)
- **DEBUG = True**: Development mode
- **Database**: SQLite (`db.sqlite3`)
- **Email**: Console backend (prints to terminal)
- **CORS**: Enabled for all origins
- **Rate Limiting**: Disabled (`ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 0`)

### POKE System Settings
```python
POKE_MAX_CONTENT_LENGTH = 100           # Max POKE message length
POKE_MAX_PER_USER_PER_DAY = 5           # Daily POKE limit per user
POKE_COOLDOWN_DAYS = 30                 # Days before re-POKEing same character
POKE_CONTENT_FILTER_URLS = True         # Block URLs in POKEs
POKE_CONTENT_FILTER_EMAILS = True       # Block emails in POKEs
POKE_PROFANITY_FILTER_ENABLED = True    # Content filtering
```

### Authentication (django-allauth)
- Method: `ACCOUNT_AUTHENTICATION_METHOD = 'username_email'`
- Email verification required
- Email must be unique
- Username required

## Status Documentation Updates

**MANDATORY**: After completing ANY task, update:
1. **docs/STATUS_REPORT.md**: Change status symbols (❌ → ✅)
2. **docs/PROJECT_STATUS_SUMMARY.md**: Update statistics, move tasks to "Co działa"
3. **docs/scrum/detailed-tasks.md**: Mark acceptance criteria with `[x]`
4. **Include documentation updates in PR/commit**

Status symbols:
- ✅ Completed/Working
- ⚠️ In Progress/Needs Verification
- ❌ Not Started/Missing

## Key Documentation Files

**Before starting work, ALWAYS check**:
- `docs/PROJECT_STATUS_SUMMARY.md` - What's done, what needs work
- `docs/STATUS_REPORT.md` - Current implementation status
- `docs/architecture/implementation-guide.md` - Step-by-step guide with code examples
- `docs/scrum/detailed-tasks.md` - Detailed task breakdowns
- `.cursor/rules/always.mdc` - Critical development rules and procedures

**Architecture Documentation**:
- `docs/architecture/poke-system-architecture.md` - POKE system design
- `docs/architecture/blocking-system-architecture.md` - Blocking system design
- `docs/architecture/conversation-management-ui-architecture.md` - Messaging UI
- `docs/architecture/homepage-layout-switcher-architecture.md` - Homepage variants

## Common Pitfalls to Avoid

1. **User vs Character**: Don't confuse user-level and character-level relationships. Friendships, messages, and blocks are CHARACTER-to-CHARACTER.

2. **POKE Before Message**: Never allow direct messaging without POKE exchange first. Always check `can_send_message()`.

3. **Fixture Dependency**: E2E tests will fail without seeded data. Always run `pnpm load:fixtures` before testing.

4. **Hash ID in URLs**: Use `<nickname>-<hash_id>` for character URLs (e.g., `/character/Dragonslayer99-a1b2c3d4e5/`), not just nickname or primary key.

5. **Blocking Checks**: Always verify blocking before allowing POKEs, messages, or friend requests using `is_blocked()`.

6. **Status Documentation**: Don't forget to update status docs after completing tasks. This is not optional.

7. **Migration Order**: Fixtures must be loaded in order: categories → games → users_and_characters

## Development Workflow Summary

1. **Check Status**: Read `docs/PROJECT_STATUS_SUMMARY.md` to verify task isn't already done
2. **Load Fixtures**: Run `pnpm load:fixtures` if database is empty
3. **Write Test**: Create Playwright E2E test first (TDD red phase)
4. **Implement**: Build feature to pass test (green phase)
5. **Refactor**: Clean up code (refactor phase)
6. **Verify**: Run all tests (`pnpm test:e2e`)
7. **Update Docs**: Update status documentation files
8. **Commit**: Include code + tests + doc updates in single commit

## Project Context

**Game Player Nick Finder** is a privacy-focused social platform helping gamers reconnect with old friends from various games. The character-centric architecture allows users to manage multiple gaming personas while maintaining privacy control through the POKE system and identity reveal features.

**Current Tech Stack**: Django 5.1.4, Bootstrap 5, SQLite (dev)/PostgreSQL (prod), Playwright (E2E)
**Future Migration Target**: Next.js + Cloudflare Workers + D1 + Joy UI + Tailwind CSS
