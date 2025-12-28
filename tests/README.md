# E2E Tests - Game Player Nick Finder

## Setup

1. Install Node.js dependencies:
```bash
pnpm install
```

2. Install Playwright browsers:
```bash
pnpx playwright install
```

## Running Tests

### Run all tests
```bash
pnpm test:e2e
```

### Run tests in UI mode (interactive)
```bash
pnpm test:e2e:ui
```

### Run tests in headed mode (see browser)
```bash
pnpm test:e2e:headed
```

### Debug tests
```bash
pnpm test:e2e:debug
```

## Test Structure

```
tests/
├── e2e/
│   ├── auth/                          # Authentication flow tests
│   │   ├── login.spec.ts              # (TODO: Login flow tests)
│   │   ├── logout.spec.ts             # (TODO: Logout flow tests)
│   │   ├── signup.spec.ts             # (TODO: Registration flow tests)
│   │   ├── password-reset.spec.ts     # (TODO: Password reset flow tests)
│   │   └── password-change.spec.ts    # (TODO: Password change flow tests)
│   ├── navigation/                    # Navigation menu tests
│   │   ├── navbar-authenticated.spec.ts    # (TODO: Navbar links for logged-in users)
│   │   └── navbar-unauthenticated.spec.ts  # (TODO: Navbar links for guest users)
│   ├── friends/
│   │   ├── friend-request-button.spec.ts
│   │   ├── friend-request-list.spec.ts
│   │   └── character-friend-list.spec.ts
│   ├── profile/
│   │   ├── profile-edit.spec.ts
│   │   └── user-profile-display.spec.ts
│   └── characters/
│       ├── character-profile-edit.spec.ts
│       └── character-profile-display.spec.ts
├── helpers/                           # Shared test utilities
│   └── auth-helpers.ts                # Authentication helper functions
```

## Test Coverage

### ✅ Implemented Tests

- ✅ Task 2.3.1: Friend Request Button
- ✅ Task 2.3.2: Friend Request List
- ✅ Task 2.3.3: Character Friend List
- ✅ Task 3.2.1: Profile Edit Form
- ✅ Task 3.2.2: User Profile Display
- ✅ Task 4.2.1: Character Profile Edit
- ✅ Task 4.2.2: Character Profile Display

### ❌ Missing Tests (TODO)

**Authentication & Navigation Tests** - See [Authentication Testing Architecture](../../docs/architecture/authentication-testing-architecture.md):
- ❌ Login flow tests
- ❌ Logout flow tests
- ❌ Registration (signup) flow tests
- ❌ Password reset flow tests
- ❌ Password change flow tests
- ❌ Navigation menu tests (authenticated users)
- ❌ Navigation menu tests (unauthenticated users)

## Helper Functions

**Authentication Helpers** (`tests/helpers/auth-helpers.ts`):
- `login(page, username, password)` - Login user and wait for redirect
- `logout(page)` - Logout user and wait for redirect
- `isAuthenticated(page)` - Check if user is logged in
- `isNotAuthenticated(page)` - Check if user is not logged in
- `TEST_USERS` - Test user credentials from fixtures

## Requirements

- Django server running on `http://localhost:8000`
- **MANDATORY**: Test data must be loaded from fixtures before running tests
- Load fixtures using: `pnpm load:fixtures` or `.\load_fixtures.ps1` (Windows) / `./load_fixtures.sh` (Unix)
- Playwright will automatically start the server if configured

## Test Data

**CRITICAL**: All E2E tests require seeded test data. Fixtures must be loaded before running tests.

### Loading Fixtures
```bash
# Using npm/pnpm script (cross-platform)
pnpm load:fixtures

# Windows PowerShell
.\load_fixtures.ps1

# Unix/Linux/MacOS
./load_fixtures.sh
```

### Test Users
- `testuser` / `testpass123` - Main test user with multiple characters
- `otheruser` / `pass` - Secondary test user
- `privateuser` / `testpass123` - User with private profile

See [TEST_FIXTURES.md](../docs/TEST_FIXTURES.md) for complete fixture documentation.

## Notes

- Tests use test data from fixtures
- Some tests check for conditional visibility (if elements exist)
- Adjust test data URLs based on your fixtures
- If you get unique constraint errors, flush database first: `pipenv run python manage.py flush --noinput`
