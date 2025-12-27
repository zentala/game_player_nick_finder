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
```

## Test Coverage

All implemented features have E2E tests:

- ✅ Task 2.3.1: Friend Request Button
- ✅ Task 2.3.2: Friend Request List
- ✅ Task 2.3.3: Character Friend List
- ✅ Task 3.2.1: Profile Edit Form
- ✅ Task 3.2.2: User Profile Display
- ✅ Task 4.2.1: Character Profile Edit
- ✅ Task 4.2.2: Character Profile Display

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
